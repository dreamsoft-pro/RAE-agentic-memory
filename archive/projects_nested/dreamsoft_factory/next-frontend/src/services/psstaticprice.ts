import api from "@/lib/api";

export default class StaticPrice {
  private groupID: number;
  private typeID: number;
  private formatID: number;
  private resource: string;

  constructor(groupID: number, typeID: number, formatID: number) {
    this.groupID = groupID;
    this.typeID = typeID;
    this.formatID = formatID;
    this.resource = `ps_groups/${groupID}/ps_types/${typeID}/ps_formats/${formatID}/ps_static_prices`;
  }

  public async getAll(force?: boolean): Promise<any> {
    const cacheKey = this.resource;

    if (force === false && localStorage.getItem(cacheKey)) {
      return JSON.parse(localStorage.getItem(cacheKey)!);
    } else {
      try {
        const response = await api.get(`${this.resource}`);
        localStorage.setItem(cacheKey, JSON.stringify(response.data));
        return response.data;
      } catch (error) {
        throw error;
      }
    }
  }
}