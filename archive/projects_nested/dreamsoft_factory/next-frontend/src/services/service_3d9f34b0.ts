import { useEffect } from 'react';
import axios from 'axios';

interface RootState {
    logged: boolean;
    myZoneStartPoint?: string;
    emitCreditLimitReload?: (value: boolean) => void;
}

const useSelectCurrency = ({ user, rootState }: { user: { userID: number }, rootState: RootState }) => {
    useEffect(() => {
        const fetchCurrency = async () => {
            try {
                await selectCurrency(user.userID);
                rootState.logged = true;

                if (rootState.emitCreditLimitReload) {
                    rootState.emitCreditLimitReload(true);
                }

                let startPoint = 'client-zone-orders';
                if (rootState.myZoneStartPoint) {
                    startPoint = rootState.myZoneStartPoint;
                }
            } catch (error) {
                console.error('Error selecting currency:', error);
            }
        };

        fetchCurrency();
    }, [user.userID, rootState.emitCreditLimitReload]);
};

const selectCurrency = async (userID: number): Promise<void> => {
    // Implement the logic to select currency for a given userID
    await axios.get(`https://api.example.com/currency/${userID}`);
};