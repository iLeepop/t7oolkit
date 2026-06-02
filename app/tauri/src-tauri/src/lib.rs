mod config;
mod tools;

use config::{load_config, save_config};
use tools::batch_resize_images_command;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            load_config,
            save_config,
            batch_resize_images_command,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
