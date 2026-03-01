import { $q } from './httpBridge';
/**
 * Service: PsFormatService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Restangular } from 'restangular';
import { $q } from 'ngimport';
import { CacheFactory } from 'angular-cache';

const cache = CacheFactory('ps_formats');

class FormatService {
    groupID: string;
    typeID: string;

    constructor(groupID: string, typeID: string) {
        this.groupID = groupID;
        this.typeID = typeID;
    }

    getResource(): string {
        return `ps_groups/${this.groupID}/ps_types/${this.typeID}/ps_formats`;
    }

    async getPublic(complexID: string, force: boolean): Promise<any> {
        const resource = this.getResource() + '/formatsPublic/' + complexID;

        if (cache.get(resource) && !force) {
            return cache.get(resource);
        } else {
            try {
                const data = await Restangular.all(resource).getList();
                cache.put(resource, data.plain());
                return data.plain();
            } catch (error) {
                throw error;
            }
        }
    }

    async getCustomNames(): Promise<any> {
        const resource = 'ps_formats';

        try {
            const data = await Restangular.all(resource).one('customName', this.typeID).get();
            return data.plain();
        } catch (error) {
            throw error;
        }
    }
}

export default FormatService;
