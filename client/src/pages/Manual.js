import '../style/Manual.css'

const Manual = () => {
    return (
        <div className="Manual">
            <h1 className="ManualText">[ MANUAL - WORK IN PROGRESS ]</h1>
            <iframe src="" frameborder="0"></iframe>
            <div dangerouslySetInnerHTML={{__html: '/Huisstijlhandboek_Kynda.html'}} />
        </div>
    )
};

export default Manual;