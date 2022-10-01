#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use tauri::api::process::{Command, CommandEvent};
#[tauri::command]
fn encrypt() {

    tauri::async_runtime::spawn(async move {

      let (mut rx, mut child) = Command::new("python3")
        .args(["./test.py"])
        .spawn()
        .expect("Failed to spawn python");


    let mut i = 0;
    while let Some(event) = rx.recv().await {
        if let CommandEvent::Stdout(line) = event {
          println!("got: {}", line);
          i += 1;
          if i == 4 {
            child.write("message from Rust\n".as_bytes()).unwrap();
            i = 0;
          }
        }
    }
    });
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
        .invoke_handler(tauri::generate_handler![choose_file, encrypt])
        .plugin(tauri_plugin_window_state::Builder::default().build())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
