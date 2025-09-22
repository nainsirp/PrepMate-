/**
 * WebRTC handler for group discussions
 */

class WebRTCHandler {
    constructor(roomId, userId, username) {
        this.roomId = roomId;
        this.userId = userId;
        this.username = username;
        this.localStream = null;
        this.peerConnections = {};
        this.participants = {};
        
        this.configuration = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
                { urls: 'stun:stun1.l.google.com:19302' }
            ]
        };
    }
    
    async initialize() {
        try {
            // Get local media stream
            this.localStream = await navigator.mediaDevices.getUserMedia({ 
                video: true, 
                audio: true 
            });
            
            return this.localStream;
        } catch (error) {
            console.error('Error accessing media devices:', error);
            throw error;
        }
    }
    
    toggleVideo(enabled) {
        this.localStream.getVideoTracks().forEach(track => {
            track.enabled = enabled;
        });
    }
    
    toggleAudio(enabled) {
        this.localStream.getAudioTracks().forEach(track => {
            track.enabled = enabled;
        });
    }
    
    // Add a participant to the list
    addParticipant(userId, username) {
        this.participants[userId] = username;
    }
    
    // Remove a participant
    removeParticipant(userId) {
        delete this.participants[userId];
        if (this.peerConnections[userId]) {
            this.peerConnections[userId].close();
            delete this.peerConnections[userId];
        }
        
        // Remove video element
        const videoEl = document.getElementById(`video-${userId}`);
        if (videoEl) {
            videoEl.parentElement.remove();
        }
    }
    
    // Clean up resources
    cleanup() {
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => track.stop());
        }
        
        Object.values(this.peerConnections).forEach(pc => {
            pc.close();
        });
        
        this.peerConnections = {};
    }
}

// Export for use in other files
window.WebRTCHandler = WebRTCHandler;
            console.error('Error creating peer connection:', error);
            throw error;
        }
    }
}

// Export for use in other files
window.WebRTCHandler = WebRTCHandler;
