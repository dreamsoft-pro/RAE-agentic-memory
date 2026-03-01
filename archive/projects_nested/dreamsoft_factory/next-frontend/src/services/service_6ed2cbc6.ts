import api from "@/lib/api";

interface Country {
  code: string;
  areaCode: string;
}

export default class AddressesEditController {
  countries: Country[] = [];
  form: { countryCode?: string; areaCode?: string } = {};

  constructor(private modalInstance) {}

  async addressesEdit() {
    try {
      const response = await api.getCountries();
      this.countries = response.data;

      // Logic to pre-populate form based on existing data
      // Assuming there's some existing data that needs to be fetched and set in the form
      if (this.form.countryCode) {
        const country = _.find(this.countries, { code: this.form.countryCode });
        if (country && String(country.areaCode).length > 0) {
          this.form.areaCode = country.areaCode;
        }
      }

      // Show modal with pre-populated form
      await this.modalInstance.show({
        countries: this.countries,
        form: this.form
      });

    } catch (error) {
      console.error("Failed to fetch countries", error);
    }
  }

  cancel() {
    this.modalInstance.close();
  }

  isCountryCode(): boolean {
    const country = _.find(this.countries, { code: this.form.countryCode });
    return Boolean(country && String(country.areaCode).length > 0);
  }

  updateAreaCode() {
    const country = _.find(this.countries, { code: this.form.countryCode });
    if (country) {
      this.form.areaCode = country.areaCode;
    }
  }
}