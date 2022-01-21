export default function CheckFile(file) {
    //Checks what kind of file is recieved as parameter
    if (file.name.includes('.png') || file.name.includes('.jpg') || file.name.includes('.jpeg')) {
        return "image"
    }
    else if (file.name.includes('.css')) {
        return "css"
    }
    else if (file.name.includes('.html')) {
        return "html"
    }
}