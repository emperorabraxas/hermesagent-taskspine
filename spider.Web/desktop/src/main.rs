// spider.Web Desktop — Tauri native wrapper
// Opens localhost:8420 in a native window (no browser chrome)

#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    tauri::Builder::default()
        .run(tauri::generate_context!())
        .expect("error running spider.Web");
}
