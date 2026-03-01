import React, { useState, useEffect } from "react";
import api from "@/lib/api";
import { toast } from "react-toastify";

/**
 * Modernized Types Management component for Next.js 14+
 * Built by the Council of Elders (Claude 4.5 + GPT-4o)
 */

export default function TypesPage({ currentGroupID }: { currentGroupID: string }) {
    const [selectedPriceListID, setSelectedPriceListID] = useState<string | null>(null);
    const [selectedNatureID, setSelectedNatureID] = useState<string | null>(null);
    const [margins, setMargins] = useState<any[]>([]);
    const [marginForm, setMarginForm] = useState<any>({});

    /**
     * Load margins based on selections
     */
    const loadMargins = async () => {
        if (!selectedPriceListID || !selectedNatureID) return;
        try {
            const data = await api.get(`margins/${selectedPriceListID}/${selectedNatureID}/${currentGroupID}`);
            setMargins(data);
        } catch (error) {
            toast.error("Error loading margins");
        }
    };

    useEffect(() => {
        loadMargins();
    }, [selectedPriceListID, selectedNatureID]);

    /**
     * Copy a type
     */
    const copyType = async (typeID: string) => {
        try {
            const data = await api.post(`types/${typeID}/copy`);
            if (data.response) {
                toast.success("Copied successfully");
                // Trigger refresh logic
            }
        } catch (error) {
            toast.error("Error copying type");
        }
    };

    /**
     * Save QuestionOnly flag
     */
    const saveQuestionOnly = async (typeID: string, isQuestionOnly: boolean) => {
        try {
            await api.patch(`types/${typeID}/question-only`, { isQuestionOnly, groupID: currentGroupID });
            toast.success("Updated successfully");
        } catch (error) {
            toast.error("Error updating type");
        }
    };

    /**
     * Add a new margin
     */
    const addMargin = async () => {
        try {
            const data = {
                ...marginForm,
                priceTypeID: selectedPriceListID,
                natureID: selectedNatureID,
                groupID: currentGroupID
            };
            const res = await api.post('margins', data);
            if (res.response) {
                toast.success("Margin added");
                setMarginForm({});
                loadMargins();
            }
        } catch (error) {
            toast.error("Error adding margin");
        }
    };

    return (
        <div>
            <h1>Types Management</h1>
            {/* UI Implementation */}
        </div>
    );
}
