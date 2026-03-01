javascript
import { ApiPaginationConfig } from '@/lib/api/pagination/config';

export class ApiPagination {
  constructor(config: ApiPaginationConfig) {
    this.config = config;
    this.currentPage = 1;
  }

  getCurrentPage(): number {
    return this.currentPage;
  }

  setPage(num: number): void {
    // [BACKEND_ADVICE] Ensure num is a positive integer and within the range of total pages
    if (num > 0 && num <= this.config.totalPages) {
      this.currentPage = num;
    }
  }

  hasPrevPage(): boolean {
    return this.currentPage !== 1;
  }

  hasNextPage(): boolean {
    // [BACKEND_ADVICE] Check against totalPages to avoid unnecessary calculations
    return this.currentPage < this.config.totalPages;
  }

  setPrevPage(): void {
    if (this.hasPrevPage()) {
      this.setPage(this.currentPage - 1);
    }
  }

  setNextPage(): void {
    if (this.hasNextPage()) {
      this.setPage(this.currentPage + 1);
    }
  }

  getTotalItems(): number {
    return this.config.totalItems;
  }
}
