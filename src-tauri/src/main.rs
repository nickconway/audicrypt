#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use tauri::api::dialog;
#[tauri::command]
async fn choose_file() -> String {
    let exts = ["mp3", "wav", "ogg", "flac"];
    let file = dialog::blocking::FileDialogBuilder::new().add_filter("Audio", &exts).pick_file();
    let path = match file {
        Some(p) => p.into_os_string().into_string().unwrap(),
        None => "".into()
    };
    return path;
}

// async fn handle_client(stream: TcpStream) {
//     println!("Incoming");
// }

// use std::net::{TcpListener, TcpStream};
#[tauri::command]
async fn open_socket() {
    // let listener = TcpListener::bind("127.0.0.1:11123").unwrap();

    // accept connections and process them serially
    // for stream in listener.incoming() {
    //     handle_client(stream.unwrap());
    // }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![choose_file, open_socket])
        .plugin(tauri_plugin_window_state::Builder::default().build())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
