/**
 * Service: MenuTypesService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { createContext, useContext, useState } from 'react';
import _ from 'lodash';

interface MenuType {
    ID: number;
    name: string;
    names?: { [key: string]: string };
    types?: MenuType[];
    groups?: GroupType[];
}

interface GroupType {
    types?: MenuType[];
}

const RootContext = createContext({ currentLang: {} as { code: string } });

export const useRootContext = () => useContext(RootContext);

function checkChilds(childs: MenuType[]): MenuType[] {
    let filtered: MenuType[] = [];
    _.each(childs, (child) => {
        if (!_.isUndefined(child.groups) && !_.isNull(child.groups) && !_.isEmpty(child.groups)) {
            filtered = _.union(filtered, checkGroups(child.groups));
        }
        if (!_.isUndefined(child.types) && !_.isNull(child.types) && !_.isEmpty(child.types)) {
            filtered = _.union(filtered, child.types);
        }
    });
    return filtered;
}

function checkGroups(groups: GroupType[]): MenuType[] {
    let filtered: MenuType[] = [];
    _.each(groups, (group) => {
        if (!_.isNull(group) && !_.isUndefined(group.types) && !_.isEmpty(group.types)) {
            filtered = _.union(filtered, group.types);
        }
    });
    return filtered;
}

function removeDuplicates(originalArray: MenuType[], prop: keyof MenuType): MenuType[] {
    let newArray: MenuType[] = [];
    const lookupObject: { [key: string]: MenuType } = {};

    for (const item of originalArray) {
        lookupObject[item[prop] as any] = item;
    }

    for (const key in lookupObject) {
        newArray.push(lookupObject[key]);
    }
    return newArray;
}

function checkMainCategory(items: MenuType[]): MenuType[] {
    if (!items || _.isEmpty(items)) {
        return [];
    }
    let types: MenuType[] = [];
    _.each(items, (item) => {
        let filtered: MenuType[] = [];
        if (!_.isUndefined(item.childs) && !_.isNull(item.childs) && !_.isEmpty(item.childs)) {
            filtered = _.union(filtered, checkChilds(item.childs));
        }
        if (!_.isUndefined(item.groups) && !_.isNull(item.groups) && !_.isEmpty(item.groups)) {
            filtered = _.union(filtered, checkGroups(item.groups));
        }
        if (!_.isUndefined(item.types) && !_.isNull(item.types) && !_.isEmpty(item.types)) {
            filtered = _.union(filtered, item.types);
        }
        filtered = _.sortBy(_.uniqBy(filtered, (item) => item.ID), (item) => {
            const rootContext = useRootContext();
            if (item.names && rootContext.currentLang && rootContext.currentLang.code) {
                return item.names[rootContext.currentLang.code];
            }
            return item.name;
        });
        types.push(...filtered);
    });
    types = removeDuplicates(types, "ID");
    return _.sortBy(types, (a) => a.name);
}

function getAllTypes(categories: MenuType[]): MenuType[] {
    let allTypes: MenuType[] = [];
    if (categories.length > 0) {
        allTypes.push(...checkMainCategory(categories));
    }
    return allTypes;
}

export default function MenuTypesService() {
    const [allTypes, setAllTypes] = useState<MenuType[]>([]);

    useEffect(() => {
        // Assuming you have a way to fetch categories or get them from props/context
        const categories: MenuType[] = []; // Fetch or get your categories here
        const types = getAllTypes(categories);
        setAllTypes(types);
    }, []);

    return { allTypes, setAllTypes };
}