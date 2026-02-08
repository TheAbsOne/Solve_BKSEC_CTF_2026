// Check password here 
const correctPassword = [-4, 11, 8, 10, 31, 0, 28, 4, 1, 25, 10, 11];

function checkPassword() {
    const dials = document.querySelectorAll('.dial');
    const enteredPassword = Array.from(dials).map(dial => Number(dial.value));
    const decodedPassword = [
        enteredPassword[0] * enteredPassword[1] - 2 * enteredPassword[2],
        enteredPassword[1] + 5 * enteredPassword[2] - 3 * enteredPassword[3],
        enteredPassword[2] + enteredPassword[3] * enteredPassword[4] - enteredPassword[0],
        enteredPassword[5] + 2 * enteredPassword[4] + enteredPassword[2],
        20 * enteredPassword[1] - 2 * enteredPassword[2] - enteredPassword[4],
        enteredPassword[2] + enteredPassword[5] - 2 * enteredPassword[1],
        2 * enteredPassword[1] + enteredPassword[2] + 3 * enteredPassword[6] + 4 * enteredPassword[7],
        5 * enteredPassword[5] - enteredPassword[7] - enteredPassword[8] + 2 * enteredPassword[9],
        3 * enteredPassword[8] + 2 * enteredPassword[9] + 4 * enteredPassword[10] - 3 * enteredPassword[6],
        9 * enteredPassword[11] + 2 * enteredPassword[10] - enteredPassword[8],
        4 * enteredPassword[7] - enteredPassword[8] + enteredPassword[10],
        enteredPassword[3] ** enteredPassword[8] + 3 * enteredPassword[11] - 2 * enteredPassword[7] + enteredPassword[6] + enteredPassword[5] + enteredPassword[10],
    ];
    if (JSON.stringify(decodedPassword) === JSON.stringify(correctPassword)) {
        const passwordString = enteredPassword.join('');
        const hexPassword = new TextEncoder().encode(passwordString).reduce((prev, curr) => prev + curr.toString(16).padStart(2, '0'), '');
        const base64Password = btoa(hexPassword);
        alert("Má»Ÿ khÃ³a thÃ nh cÃ´ng! Cá» cá»§a báº¡n lÃ  BKSEC{" + base64Password + "}");
    } else {
        alert('Máº­t kháº©u khÃ´ng chÃ­nh xÃ¡c. Vui lÃ²ng thá»­ láº¡i.');
    }
}