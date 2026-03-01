import api from "@/lib/api";
import { useState, useEffect } from "react";

const YourComponent = () => {
  const [customVolume, setCustomVolume] = useState({ custom: "", maxVolume: "" });

  const fetchVolumes = async (data: any) => {
    try {
      if (typeof data.volumeInfo === 'object') {
        setCustomVolume({
          custom: data.volumeInfo.custom,
          maxVolume: data.volumeInfo.maxVolume
        });
        
        // Simulate getting min volume
        await getMinVolume();
      } else {
        console.log("Data or Volume Info is not properly formatted.");
      }
    } catch (error) {
      console.error(error);
      Notification.error(`Error: ${error.message}`);
    }
  };

  const getMinVolume = async () => {
    // Your logic to fetch min volume here using the api module.
    // Example:
    try {
      const response = await api.get('/min-volume');
      console.log('Fetched min volume:', response.data);
    } catch (error) {
      console.error("Failed to get min volume", error.message);
    }
  };

  useEffect(() => {
    // Simulating the showVolumes function call
    fetchVolumes({ volumeInfo: { custom: "someCustomValue", maxVolume: "10" } });
  }, []);

  return (
    <div>
      {/* Your component JSX */}
    </div>
  );
};

export default YourComponent;