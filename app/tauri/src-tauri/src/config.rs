use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::fs;
use std::path::PathBuf;

const MIN_THREAD_COUNT: u32 = 1;
const MAX_THREAD_COUNT: u32 = 32;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppConfig {
    pub thread_count: u32,
    pub export_dir: String,
    #[serde(default)]
    pub tauri: Value,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            thread_count: 4,
            export_dir: default_export_dir(),
            tauri: json!({}),
        }
    }
}

fn default_export_dir() -> String {
    if let Some(downloads) = dirs::download_dir() {
        return downloads.to_string_lossy().into_owned();
    }
    dirs::home_dir()
        .map(|path| path.to_string_lossy().into_owned())
        .unwrap_or_default()
}

fn config_path() -> PathBuf {
    if cfg!(target_os = "windows") {
        dirs::config_dir()
            .or_else(dirs::home_dir)
            .unwrap_or_else(|| PathBuf::from("."))
            .join("t7oolkit")
            .join("config.json")
    } else {
        dirs::home_dir()
            .unwrap_or_else(|| PathBuf::from("."))
            .join(".config")
            .join("t7oolkit")
            .join("config.json")
    }
}

fn clamp_thread_count(value: u32) -> u32 {
    value.clamp(MIN_THREAD_COUNT, MAX_THREAD_COUNT)
}

impl AppConfig {
    pub fn load() -> Self {
        let path = config_path();
        if !path.exists() {
            return Self::default();
        }

        let content = match fs::read_to_string(&path) {
            Ok(content) => content,
            Err(_) => return Self::default(),
        };

        let data: Value = match serde_json::from_str(&content) {
            Ok(data) => data,
            Err(_) => return Self::default(),
        };

        let thread_count = data
            .get("thread_count")
            .and_then(|value| value.as_u64())
            .map(|value| value as u32)
            .unwrap_or(4);

        let export_dir = data
            .get("export_dir")
            .and_then(|value| value.as_str())
            .map(str::to_owned)
            .unwrap_or_else(default_export_dir);

        let tauri = data
            .get("tauri")
            .cloned()
            .unwrap_or_else(|| json!({}));

        Self {
            thread_count: clamp_thread_count(thread_count),
            export_dir,
            tauri,
        }
    }

    pub fn save(&self) -> Result<(), String> {
        let path = config_path();
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent).map_err(|err| err.to_string())?;
        }

        let existing: Value = if path.exists() {
            fs::read_to_string(&path)
                .ok()
                .and_then(|content| serde_json::from_str(&content).ok())
                .unwrap_or_else(|| json!({}))
        } else {
            json!({})
        };

        let mut data = existing.as_object().cloned().unwrap_or_default();
        data.insert(
            "thread_count".to_string(),
            json!(clamp_thread_count(self.thread_count)),
        );
        data.insert("export_dir".to_string(), json!(self.export_dir));
        data.insert("tauri".to_string(), self.tauri.clone());

        let output = serde_json::to_string_pretty(&Value::Object(data)).map_err(|err| err.to_string())?;
        fs::write(path, output).map_err(|err| err.to_string())
    }
}

#[tauri::command]
pub fn load_config() -> AppConfig {
    AppConfig::load()
}

#[tauri::command]
pub fn save_config(config: AppConfig) -> Result<(), String> {
    config.save()
}
