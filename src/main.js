const { invoke } = window.__TAURI__.tauri;
const { Command } = window.__TAURI__.shell

let encryption_file;
let decryption_file;

async function choose_file_encryption() {
    encryption_file = await invoke("choose_file", {});
    document.querySelector("#encryption-msg").textContent = encryption_file;
}

async function choose_file_decryption() {
    decryption_file = await invoke("choose_file", {});
    document.querySelector("#decryption-msg").textContent = decryption_file;
}

async function encrypt() {
    console.log("encrypting");
    const command = new Command("run-py", ["-e", "text", "test.mp3"]);
    command.on('close', data => {
      console.log(`command finished with code ${data.code} and signal ${data.signal}`)
    });
    command.on('error', error => console.error(`command error: "${error}"`));
    command.stdout.on('data', line => console.log(`command stdout: "${line}"`));
    command.stderr.on('data', line => console.log(`command stderr: "${line}"`));

    const child = await command.spawn();
    console.log('pid:', child.pid);
    await invoke ("encrypt", {});
}

async function decrypt() {
    await invoke ("decrypt", {});
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
window.encrypt = encrypt;
window.decrypt = decrypt;
window.toggle_type = toggle_type;
