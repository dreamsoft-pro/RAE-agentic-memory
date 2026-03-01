import React, { useRef, useState } from 'react';
import ModalContent from "./components/ModalContent";
import ModalHeader from "./components/ModalHeader";
import ModalBody from "./components/ModalBody";

const HeaderVideosModal = ({ id }) => {
    //Example videos tab
    const videoUrls = [
        "https://www.w3schools.com/html/mov_bbb.mp4", 
        "https://www.w3schools.com/html/mov_bbb.mp4",
        "https://www.w3schools.com/html/mov_bbb.mp4",
        "https://www.w3schools.com/html/mov_bbb.mp4",
        "https://www.w3schools.com/html/mov_bbb.mp4",
        "https://www.w3schools.com/html/mov_bbb.mp4"
    ];

    const videoRefs = useRef(Array(videoUrls.length).fill(null)); 
    const [playingVideos, setPlayingVideos] = useState(Array(videoUrls.length).fill(false));

    const handlePlayVideo = (index) => {
        const videoRef = videoRefs.current[index];
        if (videoRef) {
            videoRef.play();
            videoRef.controls = true; 

            setPlayingVideos((prev) => {
                const newPlayingVideos = [...prev];
                newPlayingVideos[index] = true; 
                return newPlayingVideos;
            });
        }
    };

    const handleCloseModal = () => {
        setPlayingVideos(Array(videoUrls.length).fill(false));
        videoRefs.current.forEach(videoRef => {
            if (videoRef) {
                videoRef.pause(); 
                videoRef.currentTime = 0; 
            }
        });
    };

    return (
        <ModalContent id={"videosModal"} className={"modal-xl"}>
            <ModalHeader
                title={"Wideo instruktażowe dotyczące obsługi edytora"}
                onCancel={handleCloseModal}
            >
                <div className={'modal-icon'}>?</div>
            </ModalHeader>
            <ModalBody>
                <div className={'modal-nav-header-container'}>
                    <div className="modal-videos-grid">
                        {videoUrls.map((url, index) => {
                            return (
                                <div key={index} className="video-block">
                                    <video
                                        ref={el => videoRefs.current[index] = el}
                                        src={url}
                                        className="video-player"
                                        controls={playingVideos[index]}
                                    />
                                    {!playingVideos[index] && (
                                        <button
                                            className="play-button"
                                            onClick={() => handlePlayVideo(index)}
                                        >
                                        </button>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                </div>
            </ModalBody>
        </ModalContent>
    );
};

export default HeaderVideosModal;
