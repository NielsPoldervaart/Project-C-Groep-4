import CheckFile from "./CheckFile";

export default async function readFile(file) {
    if (CheckFile(file) === "image") {
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