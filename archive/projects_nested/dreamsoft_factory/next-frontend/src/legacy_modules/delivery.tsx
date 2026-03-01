/**
 * Service: delivery
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';

interface Address {
    weight: number;
    price: number;
}

interface Currency {
    symbol: string;
}

interface ProductAddress {
    volume: number;
    deliveryID: number;
    allVolume: number;
    no_of_pkgs: number;
    grossweight: number;
}

const DeliveryComponent = () => {
    const [addresses, setAddresses] = useState<Address[]>([]);
    const [currentCurrency, setCurrentCurrency] = useState<Currency>({ symbol: '' });
    const [productAddresses, setProductAddresses] = useState<ProductAddress[]>([]);
    const [separateVolume, setSeparateVolume] = useState<number | null>(null);
    const [logged, setLogged] = useState(false);
    const [oneTimeUser, setOneTimeUser] = useState(false);
    const [deliveryLackOfVolume, setDeliveryLackOfVolume] = useState(0);
    const [productItem, setProductItem] = useState<{ volume: number }>({ volume: 0 });
    const [senders, setSenders] = useState([]);

    useEffect(() => {
        // Fetch data from API or state management
        axios.get('/api/addresses').then(response => {
            setAddresses(response.data);
        });
        axios.get('/api/currency').then(response => {
            setCurrentCurrency(response.data);
        });
        axios.get('/api/productAddresses').then(response => {
            setProductAddresses(response.data);
        });
        axios.get('/api/senders').then(response => {
            setSenders(response.data);
        });
    }, []);

    const removeProductAddress = (index: number) => {
        // Remove product address logic
    };

    const separateDelivery = () => {
        // Separate delivery logic
    };

    return (
        <div>
            <table className="table">
                <tbody>
                    {productAddresses.map((address, index) => (
                        <tr key={index}>
                            <td>{address.weight} kg</td>
                            <td className="col-price">{address.price} {currentCurrency.symbol}</td>
                            {/* Add more columns as needed */}
                        </tr>
                    ))}
                </tbody>
            </table>

            {logged && !oneTimeUser && (deliveryLackOfVolume > 0 || productItem.volume > 1) && (
                <div className="col-md-6 col-sm-6">
                    {deliveryLackOfVolume > 0 ? (
                        <div className="alert alert-danger">
                            {/* delivery_lack_of_volume */}
                            {deliveryLackOfVolume}
                        </div>
                    ) : null}
                </div>
            )}

            {productItem.volume > 1 && addresses.length > 0 ? (
                <div className="col-md-6 col-sm-6">
                    <div className="input-group">
                        <input type="text" placeholder="separate_volume" className="form-control" value={separateVolume} onChange={(e) => setSeparateVolume(Number(e.target.value))} />
                        <span onClick={separateDelivery} className="input-group-addon btn">
                            <i className="fa fa-plus"></i> separate_delivery
                        </span>
                    </div>
                </div>
            ) : null}
        </div>
    );
};

export default DeliveryComponent;