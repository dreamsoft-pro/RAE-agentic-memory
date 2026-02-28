import { useEffect, useState } from 'react';
import axios from '@/lib/api'; // Assuming this is an Axios instance

export default class RoleService {
  private static instance: RoleService;

  private constructor() {}

  public static getInstance(): RoleService {
    if (!RoleService.instance) {
      RoleService.instance = new RoleService();
    }
    return RoleService.instance;
  }

  public async getAllRoles(): Promise<any[]> {
    try {
      const response = await axios.get('/roles');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch roles', error);
      throw error;
    }
  }

  public async getRolePerms(id: number): Promise<any> {
    try {
      const response = await axios.get(`/roles/${id}/rolePerms`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch role perms', error);
      throw error;
    }
  }

  public async updateSelectedRolePerms(id: number, selected: any[]): Promise<any> {
    try {
      const response = await axios.post(`/roles/${id}/rolePerms`, selected);
      return response.data;
    } catch (error) {
      console.error('Failed to update role perms', error);
      throw error;
    }
  }

  public async createRole(group: any): Promise<any> {
    try {
      const response = await axios.post('/roles', group);
      return response.data;
    } catch (error) {
      console.error('Failed to create new role', error);
      throw error;
    }
  }
}