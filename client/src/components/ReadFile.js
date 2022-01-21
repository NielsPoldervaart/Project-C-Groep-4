import CheckFile from "./CheckFile";

export default async function readFile(file) {
    if (CheckFile(file) === "image") {
        // Returns a promise with the result being the DataURL of an image
        return new Promise((resolve, reject) => {
            let fr = new FileReader();  

            fr.onload = () => {
              resolve(fr.result)
            };
            fr.onerror = reject;

            fr.readAsDataURL(file);
        });
    }
    else if (CheckFile(file) === "html" || CheckFile(file) === "css") {
        // Returns a promise with the result being the string of the html or css file
        return new Promise((resolve, reject) => {
            let fr = new FileReader();  

            fr.onload = () => {
              resolve(fr.result)
            };
            fr.onerror = reject;

            fr.readAsBinaryString(file);
        });
    }
}