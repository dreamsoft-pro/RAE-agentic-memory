javascript
'use strict';

import { Api } from '@/lib/api';
import { CACHE_MANAGER } from '@nestjs/cache-manager';
import { Inject, Injectable } from '@nestjs/common';
import { firstValueFrom, Observable } from 'rxjs';

@Injectable()
export class PsStaticPriceService {
  constructor(@Inject(CACHE_MANAGER) private cacheManager: any, private api: Api) {}

  getAll(groupID: string, typeID: string, formatID: string, force = false): Observable<any> {
    const resource = `ps_groups/${groupID}/ps_types/${typeID}/ps_formats/${formatID}/ps_static_prices`;

    return this.cacheManager.get(resource).pipe(
      firstValueFrom({
        fallbackNext: () => {
          if (!force) {
            throw new Error('Cache not available or force is false');
          }
          return this.api.get<any>(resource);
        },
        fallbackError: (error) => {
          console.error(error);
          throw error;
        }
      })
    );
  }

  static create(groupID: string, typeID: string, formatID: string): PsStaticPriceService {
    return new PsStaticPriceService(null, { get: (resource: string) => ({}) });
  }
}
