import api from '@/lib/api';
import { useState, useEffect } from 'react';

interface AddressForm {
  saving: boolean;
  type?: number;
}

const addressService = {
  addAddress: async (form: any) => await api.post('/api/address/add', form),
  saveAddressToSession: async (addressID: string | number) => await api.post(`/api/session/save/${addressID}`)
};

export default function AddressFormComponent() {
  const [countries, setCountries] = useState([]);
  const [form, setForm] = useState<AddressForm>({ saving: false });
  const [addresses, setAddresses] = useState([]);

  const addAddress = async () => {
    try {
      form.saving = true;
      form.type = 1;

      const response = await addressService.addAddress(form);

      if (response.data.response === true) {
        setForm({});
        setForm(prevForm => ({ ...prevForm, saving: false }));
        setAddresses(prevAddresses => [...prevAddresses, response.data.item]);
        await addressService.saveAddressToSession(response.data.addressID);
        Notification.success('saved'); // Assuming Notification is a global or imported service
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    // Fetch countries on component mount if needed
    api.get('/api/countries').then(data => setCountries(data.data));
  }, []);

  return (
    <div>
      {/* Render form and other UI elements here */}
    </div>
  );
}