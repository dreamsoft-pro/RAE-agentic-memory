/**
 * Service: address-modal
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { Modal, Form, Input } from 'antd';

const AddressModal = ({ visible, onCancel, form }) => {
    const [form] = Form.useForm();

    return (
        <Modal 
            title="Addresses" 
            visible={visible} 
            onCancel={onCancel} 
            footer={[
                <button key="cancel" onClick={onCancel}>Cancel</button>,
                <button key="save" type="primary" form="addressForm">Save</button>
            ]}
        >
            <Form form={form} id="addressForm" layout="vertical">
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Form.Item label="First Name" name="name" rules={[{ required: true, message: 'Please input your first name!' }]}>
                        <Input placeholder="First Name" />
                    </Form.Item>
                    <Form.Item label="Last Name" name="lastname" rules={[{ required: true, message: 'Please input your last name!' }]}>
                        <Input placeholder="Last Name" />
                    </Form.Item>
                </div>
                <Form.Item label="Street" name="street" rules={[{ required: true, message: 'Please input your street!' }]}>
                    <Input placeholder="Street" />
                </Form.Item>
                <Form.Item label="House Number" name="house">
                    <Input placeholder="House Number" />
                </Form.Item>
                <Form.Item label="Apartment Number" name="apartment">
                    <Input placeholder="Apartment Number" />
                </Form.Item>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Form.Item label="Postal Code" name="zipcode" rules={[{ required: true, message: 'Please input your postal code!' }]}>
                        <Input placeholder="Postal Code" />
                    </Form.Item>
                    <Form.Item label="City" name="city" rules={[{ required: true, message: 'Please input your city!' }]}>
                        <Input placeholder="City" />
                    </Form.Item>
                </div>
                <Form.Item label="Country Code" name="countryCode">
                    <Select placeholder="Select a country">
                        {countries.map(country => (
                            <Option key={country.code} value={country.code}>{country.name_pl}</Option>
                        ))}
                    </Select>
                </Form.Item>
                <Form.Item label="Area Code" name="areaCode">
                    <Input placeholder="+" disabled={isCountryCode()} />
                </Form.Item>
                <Form.Item label="Telephone Number" name="telephone" rules={[{ required: true, message: 'Please input your telephone number!' }]}>
                    <Input placeholder="Telephone Number" />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default AddressModal;