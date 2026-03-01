/**
 * Service: SitemapCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

To modernize the provided JavaScript file (`SitemapCtrl.js`) to TypeScript (TSX), we need to make several changes, including converting the code to use ES6+ syntax and TypeScript types. Here's how you can refactor the file:

1. **Use `import`/`export` for module imports/exports instead of Angular-specific modules.**
2. **Convert function definitions to arrow functions where appropriate.**
3. **Specify variable types using TypeScript syntax.**
4. **Utilize async/await for better readability and handling asynchronous code.**

Here's the refactored version in TSX:

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DpCategoryService } from './dp-category.service'; // Adjust according to your import path
import _ from 'lodash';
import { Observable } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-sitemap',
  templateUrl: './sitemap.component.html',
  styleUrls: ['./sitemap.component.css']
})
export class SitemapCtrl implements OnInit {
  sites: any[] = [];
  menuItems: any;

  constructor(private route: ActivatedRoute, private router: Router, private dpCategoryService: DpCategoryService) {}

  ngOnInit(): void {
    this.route.data.pipe(
      switchMap((data: any) => data.routes),
      map((routeData: any) => routeData.data)
    ).subscribe((routeData: any) => {
      if (routeData) {
        _.each(routeData, (one) => {
          if (one.route.parent === 'home' && one.route.abstract === 0 && ['sitemap', 'cart', 'attribute-filters'].includes(one.route.state)) {
            this.sites.push(one.route);
          } else if (one.route.parent === 'staticPages') {
            this.sites.push(one.route);
          }
        });
      }
    });
  }

  async getItems(): Promise<any> {
    const def = new Observable((observer) => {
      setTimeout(() => {
        if (this.menuItems !== undefined) {
          observer.next(this.menuItems);
          observer.complete();
        } else {
          observer.error('Menu items are not defined');
        }
      }, 1000);
    });

    return def;
  }

  async getGroups(): Promise<any> {
    const def = new Observable((observer) => {
      this.dpCategoryService.getGroups().subscribe({
        next: (data) => observer.next(data),
        error: (err) => observer.error(err),
        complete: () => observer.complete()
      });
    });

    return def;
  }
}


