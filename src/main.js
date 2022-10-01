const { invoke } = window.__TAURI__.tauri;
const { Command } = window.__TAURI__.shell;

let encryption_file = "";
let decryption_file = "";

async function choose_file_encryption() {
    encryption_file = await invoke("choose_file", {});
    document.querySelector("#encryption-msg").textContent = encryption_file;
}

async function choose_file_decryption() {
    decryption_file = await invoke("choose_file", {});
    document.querySelector("#decryption-msg").textContent = decryption_file;
}

async function encrypt() {
    let text = document.querySelector("#encrypt-input").value
    if (encryption_file !== "" && text !== "") {
        console.log("encrypting", encryption_file, text);
        document.querySelector("#encryption-status").textContent = "Encrypting...";
        const command = new Command("run-py-enc", ["../src-tauri/src/manip.py", "encrypt", encryption_file, text]);
        command.on('close', data => {
          console.log(`command finished with code ${data.code} and signal ${data.signal}`)
        });
        command.on('error', error => console.error(`command error: "${error}"`));
        command.stdout.on('data', line => {
            console.log(`command stdout: "${line}"`)
            document.querySelector("#encryption-status").textContent = line;
        });
        command.stderr.on('data', line => console.log(`command stderr: "${line}"`));

        const child = await command.spawn();
        console.log('pid:', child.pid);
    } else {
        document.querySelector("#encryption-status").textContent = "You must enter text to encrypt and choose a file before encrypting";
    }
}

async function decrypt() {
    if (decryption_file !== "") {
        console.log("decrypting");
        document.querySelector("#decryption-status").textContent = "Decrypting...";
        const command = new Command("run-py-dec", ["../src-tauri/src/manip.py", "decrypt", decryption_file]);
        command.on('close', data => {
          console.log(`command finished with code ${data.code} and signal ${data.signal}`)
        });
        command.on('error', error => console.error(`command error: "${error}"`));
        command.stdout.on('data', line => {
            document.querySelector("#decryption-status").textContent = line;
            console.log(`command stdout: "${line}"`)
        });
        command.stderr.on('data', line => console.log(`command stderr: "${line}"`));

        const child = await command.spawn();
        console.log('pid:', child.pid);
    } else {
        document.querySelector("#decryption-status").textContent = "You must choose a file to decrypt";
    }
}

async function show(tab) {

    document.querySelector('#encrypt_header').classList.remove("selected");
    document.querySelector('#decrypt_header').classList.remove("selected");
    document.querySelector('#send_header').classList.remove("selected");
    document.querySelector('#receive_header').classList.remove("selected");
    document.querySelector('#' + tab + "_header").classList.add("selected");

    document.querySelector('#encrypt_tab').style.display = "none";
    document.querySelector('#decrypt_tab').style.display = "none";
    document.querySelector('#send_tab').style.display = "none";
    document.querySelector('#receive_tab').style.display = "none";
    document.querySelector('#' + tab + "_tab").style.display = "flex";
    
    if (tab === "receive") {
        invoke("open_socket", {});
    }

}

window.choose_file_encryption = choose_file_encryption;
window.choose_file_decryption = choose_file_decryption;
window.encrypt = encrypt;
window.decrypt = decrypt;
window.show = show;

// geting canvas by Boujjou Achraf
var c = document.getElementById("c");
var ctx = c.getContext("2d");

//making the canvas full screen
c.height = window.innerHeight;
c.width = window.innerWidth;

//chinese characters - taken from the unicode charset
var matrix = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
//converting the string into an array of single characters
matrix = matrix.split("");

var font_size = 10;
var columns = c.width/font_size; //number of columns for the rain
//an array of drops - one per column
var drops = [];
//x below is the x coordinate
//1 = y co-ordinate of the drop(same for every drop initially)
for(var x = 0; x < columns; x++)
    drops[x] = 1; 

//drawing the characters
function draw()
{
    //Black BG for the canvas
    //translucent BG to show trail
    ctx.fillStyle = "rgba(0, 0, 0, 0.04)";
    ctx.fillRect(0, 0, c.width, c.height);

    ctx.fillStyle = "#0099ff"; // color of fill
    ctx.font = font_size + "px arial";
    //looping over drops
    for(var i = 0; i < drops.length; i++)
    {
        //a random chinese character to print
        var text = matrix[Math.floor(Math.random()*matrix.length)];
        //x = i*font_size, y = value of drops[i]*font_size
        ctx.fillText(text, i*font_size, drops[i]*font_size);

        //sending the drop back to the top randomly after it has crossed the screen
        //adding a randomness to the reset to make the drops scattered on the Y axis
        if(drops[i]*font_size > c.height && Math.random() > 0.975)
            drops[i] = 0;

        //incrementing Y coordinate
        drops[i]++;
    }
}

setInterval(draw, 35);
