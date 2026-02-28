import api from '@/lib/api';

class FileSizeConverter {
    private PHONE_SCALED_SIZE: number = 1048576 * 1024; // Assuming [PHONE]*** should be a large number like 1GB * 1024 for demonstration

    async convertFileSize(bytes: number): Promise<string> {
        if (bytes >= this.PHONE_SCALED_SIZE) {
            bytes = (bytes / this.PHONE_SCALED_SIZE).toFixed(2) + ' GB';
        } else if (bytes >= 1048576) {
            bytes = (bytes / 1048576).toFixed(2) + ' MB';
        } else if (bytes >= 1024) {
            bytes = (bytes / 1024).toFixed(2) + ' KB';
        } else if (bytes > 1) {
            bytes = bytes.toString() + ' bytes';
        } else if (bytes === 1) {
            bytes = bytes.toString() + ' byte';
        } else {
            bytes = '0 byte';
        }
        return bytes;
    }

    handleGoTop(offset: number = 300, duration: number = 500): void {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
}

// Example usage
const fileSizeConverter = new FileSizeConverter();
fileSizeConverter.convertFileSize(123456789).then(console.log);
fileSizeConverter.handleGoTop();