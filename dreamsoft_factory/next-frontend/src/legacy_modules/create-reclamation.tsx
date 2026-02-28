/**
 * Service: create-reclamation
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';
import './CreateReclamation.css'; // Assuming you have a CSS file for styling

interface Fault {
    ID: number;
    descriptions: { [key: string]: { name: string } };
}

interface Product {
    productID: number;
    type: { names: { [key: string]: string } };
}

interface FormData {
    faults: { [key: number]: boolean };
    products: number[];
    description: string;
}

interface Props {
    reclamationExist: boolean;
    reclamation?: { ID: number };
    faults: Fault[];
    products: Product[];
    uploadProgress: number;
    formData: FormData;
    save: (formData: FormData) => void;
    updateFormData: (key: keyof FormData, value: any) => void;
    removeFile: (item: any) => void;
}

const CreateReclamation: React.FC<Props> = ({ 
    reclamationExist, 
    reclamation, 
    faults, 
    products, 
    uploadProgress, 
    formData, 
    save, 
    updateFormData, 
    removeFile 
}) => {
    const { t } = useTranslation();
    const currentLang = { code: 'en' }; // Assuming you have a way to get the current language

    return (
        <div className="panel panel-default">
            <div className="panel-heading">
                <h2 className="panel-title">{t('create_reclamation_form')}</h2>
            </div>
            <div className="panel-body">
                {reclamationExist ? (
                    <div className="alert alert-info col-md-offset-3 col-md-6 text-center">
                        <span>{t('reclamation_exist')}</span><br />
                        <b>ID: {reclamation?.ID}</b>
                    </div>
                ) : (
                    <form className="form-horizontal" onSubmit={() => save(formData)}>
                        <div className="form-group">
                            <label className="col-md-3 control-label">{t('fault_description')} *</label>
                            <div className="col-md-offset-3 col-md-9">
                                {faults.map(fault => (
                                    <label key={fault.ID}>
                                        <input 
                                            type="checkbox" 
                                            checked={formData.faults[fault.ID]} 
                                            onChange={(e) => updateFormData('faults', {...formData.faults, [fault.ID]: e.target.checked})}
                                        /> {fault.descriptions[currentLang.code].name}
                                    </label>
                                ))}
                            </div>
                        </div>
                        <div className="form-group">
                            <label className="col-md-3 control-label">{t('products')} *</label>
                            <div className="col-md-9">
                                <select 
                                    multiple 
                                    className="form-control" 
                                    value={formData.products}
                                    onChange={(e) => updateFormData('products', Array.from(e.target.selectedOptions, (option: HTMLOptionElement) => parseInt(option.value)))}
                                >
                                    <option value="">{t('select')}</option>
                                    {products.map(product => (
                                        <option key={product.productID} value={product.productID}>{product.type.names[currentLang.code]}</option>
                                    ))}
                                </select>
                            </div>
                        </div>
                        <div className="form-group">
                            <label className="col-md-3 control-label" htmlFor="reclamation-description">{t('description')} *</label>
                            <div className="col-md-9">
                                <textarea 
                                    className="form-control" 
                                    value={formData.description}
                                    onChange={(e) => updateFormData('description', e.target.value)}
                                    placeholder={t('description')} 
                                    required 
                                    id="reclamation-description"
                                />
                            </div>
                        </div>
                        <div className="form-group">
                            <label className="col-md-3 control-label">{t('add_files')} *</label>
                            <div className="col-md-9">
                                <input 
                                    type="file" 
                                    multiple 
                                    onChange={(e) => console.log(e.target.files)} // Handle file upload here
                                />
                            </div>
                        </div>
                        <div className="form-group">
                            <div className="col-md-3 col-md-offset-9">
                                <button type="submit" className="btn btn-success btn-block btn-submit">{t('save')}</button>
                            </div>
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
};

export default CreateReclamation;