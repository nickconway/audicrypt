const { invoke } = window.__TAURI__.tauri;

async function choose_file_encryption() {
    document.querySelector("#encryption-msg").textContent = await invoke("choose_file", {});
}

async function choose_file_decryption() {
    document.querySelector("#decryption-msg").textContent = await invoke("choose_file", {});
}

async function toggle_type() {

    let encryption_display = getComputedStyle(document.querySelector('div.encryption'), {}).display;
    let decryption_display = getComputedStyle(document.querySelector('div.decryption'), {}).display;

    console.log(encryption_display);
    console.log(decryption_display);

    if (encryption_display === "flex") {
        document.querySelector('span.encryption').classList.remove("selected");
        document.querySelector('div.encryption').style.display = "none";
        document.querySelector('span.decryption').classList.add("selected");
        document.querySelector('div.decryption').style.display = "flex";
    } else if (decryption_display === "flex") {
        document.querySelector('span.decryption').classList.remove("selected");
        document.querySelector('div.decryption').style.display = "none";
        document.querySelector('span.encryption').classList.add("selected");
        document.querySelector('div.encryption').style.display = "flex";
    }

}

window.choose_file_encryption = choose_file_encryption;
window.choose_file_decryption = choose_file_decryption;
window.toggle_type = toggle_type;
