import api from '@/lib/api';

class TimeFormatter {
    private static formatTimePeriod(timePeriod: number, unit?: string): string {
        if (timePeriod) {
            if (unit) {
                switch (unit) {
                    case 'minutes':
                        timePeriod *= 60;
                        break;
                    default:
                        break;
                }
            }

            let d = Math.floor(timePeriod / 86400);
            timePeriod -= d * 86400;

            let h = Math.floor(timePeriod / 3600);
            timePeriod -= h * 3600;

            let m = Math.floor(timePeriod / 60);

            let formated: string = '';

            if (d > 0) {
                formated += d.toString() + 'd';
            }

            if (h > 0) {
                if (d > 0) {
                    formated += ' ';
                }
                formated += h.toString();
            }

            if (m > 0) {
                if (h > 0) {
                    formated += ':';
                }
                formated += m;
            }

            // Adding proper suffixes
            if (formated) {
                if (h > 0) {
                    formated += ' h';
                } else if (m > 0) {
                    formated += ' m';
                }
            }

            return formated || '';
        }

        return '';
    }

    // Example usage of the formatTimePeriod method
    public static async fetchAndFormatData() {
        try {
            const data = await api.get('/some-endpoint');
            const timePeriod: number = data.timePeriod; // Assuming there is a 'timePeriod' field in the returned data.
            const unit: string | undefined = data.unit; // Assuming there is an optional 'unit' field in the returned data.

            const formattedTimePeriod = TimeFormatter.formatTimePeriod(timePeriod, unit);
            console.log(formattedTimePeriod);

        } catch (error) {
            console.error('Error fetching and formatting data:', error);
        }
    }
}

// Usage
TimeFormatter.fetchAndFormatData();