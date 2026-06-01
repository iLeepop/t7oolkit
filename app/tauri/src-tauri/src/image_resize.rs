use image::imageops::FilterType;
use image::GenericImageView;
use rayon::prelude::*;
use serde::Serialize;
use std::fs;
use std::path::{Path, PathBuf};
use tauri::{AppHandle, Emitter};

const IMAGE_EXTENSIONS: &[&str] = &[
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff",
];

#[derive(Debug, Clone, Serialize)]
pub struct ResizeResult {
    pub filename: String,
    pub source_size: (u32, u32),
    pub output_size: (u32, u32),
    pub skipped: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct ResizeError {
    pub filename: String,
    pub message: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct BatchResizeResponse {
    pub results: Vec<ResizeResult>,
    pub errors: Vec<ResizeError>,
}

#[derive(Debug, Clone, Serialize)]
pub struct ResizeProgressPayload {
    pub current: usize,
    pub total: usize,
    pub filename: String,
}

pub fn list_image_files(input_dir: &Path) -> Vec<PathBuf> {
    let Ok(entries) = fs::read_dir(input_dir) else {
        return Vec::new();
    };

    let mut files: Vec<PathBuf> = entries
        .filter_map(Result::ok)
        .map(|entry| entry.path())
        .filter(|path| path.is_file())
        .filter(|path| {
            path.extension()
                .and_then(|ext| ext.to_str())
                .map(|ext| {
                    let lower = format!(".{}", ext.to_lowercase());
                    IMAGE_EXTENSIONS.contains(&lower.as_str())
                })
                .unwrap_or(false)
        })
        .collect();

    files.sort_by_key(|path| path.file_name().map(|name| name.to_ascii_lowercase()));
    files
}

fn resize_image(
    input_path: &Path,
    output_path: &Path,
    max_size: u32,
) -> Result<ResizeResult, String> {
    if let Some(parent) = output_path.parent() {
        fs::create_dir_all(parent).map_err(|err| err.to_string())?;
    }

    let img = image::open(input_path).map_err(|err| err.to_string())?;
    let (width, height) = img.dimensions();
    let source_size = (width, height);

    if width <= max_size && height <= max_size {
        img.save(output_path).map_err(|err| err.to_string())?;
        return Ok(ResizeResult {
            filename: input_path
                .file_name()
                .and_then(|name| name.to_str())
                .unwrap_or("")
                .to_string(),
            source_size,
            output_size: source_size,
            skipped: true,
        });
    }

    let ratio = (max_size as f64 / width as f64).min(max_size as f64 / height as f64);
    let new_width = (width as f64 * ratio).round() as u32;
    let new_height = (height as f64 * ratio).round() as u32;
    let resized = img.resize(new_width, new_height, FilterType::Lanczos3);
    resized.save(output_path).map_err(|err| err.to_string())?;

    Ok(ResizeResult {
        filename: input_path
            .file_name()
            .and_then(|name| name.to_str())
            .unwrap_or("")
            .to_string(),
        source_size,
        output_size: (new_width, new_height),
        skipped: false,
    })
}

pub fn batch_resize_images(
    input_dir: &Path,
    output_dir: &Path,
    max_size: u32,
    workers: usize,
    app: &AppHandle,
) -> BatchResizeResponse {
    fs::create_dir_all(output_dir).ok();

    let files = list_image_files(input_dir);
    if files.is_empty() {
        return BatchResizeResponse {
            results: Vec::new(),
            errors: Vec::new(),
        };
    }

    let pool = rayon::ThreadPoolBuilder::new()
        .num_threads(workers.max(1).min(files.len()))
        .build()
        .unwrap_or_else(|_| rayon::ThreadPoolBuilder::new().build().expect("rayon pool"));

    let total = files.len();
    let progress = std::sync::atomic::AtomicUsize::new(0);

    let outcomes: Vec<Result<ResizeResult, ResizeError>> = pool.install(|| {
        files
            .par_iter()
            .map(|path| {
                let current = progress.fetch_add(1, std::sync::atomic::Ordering::SeqCst) + 1;
                let filename = path
                    .file_name()
                    .and_then(|name| name.to_str())
                    .unwrap_or("")
                    .to_string();

                let _ = app.emit(
                    "resize-progress",
                    ResizeProgressPayload {
                        current,
                        total,
                        filename: filename.clone(),
                    },
                );

                match resize_image(path, &output_dir.join(path.file_name().unwrap_or_default()), max_size) {
                    Ok(result) => Ok(result),
                    Err(message) => Err(ResizeError { filename, message }),
                }
            })
            .collect()
    });

    let mut results = Vec::new();
    let mut errors = Vec::new();

    for outcome in outcomes {
        match outcome {
            Ok(result) => results.push(result),
            Err(error) => errors.push(error),
        }
    }

    results.sort_by_key(|item| item.filename.to_ascii_lowercase());
    errors.sort_by_key(|item| item.filename.to_ascii_lowercase());

    BatchResizeResponse { results, errors }
}

#[tauri::command]
pub fn batch_resize_images_command(
    app: AppHandle,
    input_dir: String,
    output_dir: String,
    max_size: u32,
    workers: u32,
) -> BatchResizeResponse {
    batch_resize_images(
        Path::new(&input_dir),
        Path::new(&output_dir),
        max_size,
        workers as usize,
        &app,
    )
}
