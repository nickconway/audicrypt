#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

use tauri::api::dialog;
#[tauri::command]
async fn choose_file() -> String {
    let file = dialog::blocking::FileDialogBuilder::new().pick_file();
    let path = match file {
        Some(p) => p.into_os_string().into_string().unwrap(),
        None => "".into()
    };
    return path;
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, choose_file])
        .plugin(tauri_plugin_window_state::Builder::default().build())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
