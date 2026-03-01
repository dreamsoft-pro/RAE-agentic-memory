javascript
class CalculationService {
    resource = 'calculations';

    async fetchCalculations() {
        return axios.get(`/${this.resource}`);
    }
}