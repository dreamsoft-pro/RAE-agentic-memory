
import asyncio
import os
import sys
import json
from pathlib import Path

# Fix report data (extracted from RAE memory)
REPORT_JSON = """
{"fixes_required": [{"file": "service_4bbe33b0.ts", "missing": ["UserService"]}, {"file": "service_05d8a6c4.ts", "missing": ["LangRootService"]}, {"file": "authservice.ts", "missing": ["UserService", "AuthService"]}, {"file": "invoice.ts", "missing": ["InvoiceService"]}, {"file": "service_65738d23.ts", "missing": ["AddressService"]}, {"file": "service_f104ca23.ts", "missing": ["AddressService"]}, {"file": "service_f6fa04f8.ts", "missing": ["CalculationService"]}, {"file": "service_2ad4c76d.ts", "missing": ["AuthService"]}, {"file": "userservice.ts", "missing": ["UserService"]}, {"file": "currency.ts", "missing": ["CurrencyService"]}, {"file": "domain.ts", "missing": ["DomainService"]}, {"file": "service_8a3c0871.ts", "missing": ["DeliveryService"]}, {"file": "service_8fd6aa98.ts", "missing": ["DpProductService"]}, {"file": "service_a6376450.ts", "missing": ["UserService"]}, {"file": "service_3f331b57.ts", "missing": ["UserService", "CacheService"]}, {"file": "calculationservice.ts", "missing": ["CalculationService"]}, {"file": "service_5dba6e9a.ts", "missing": ["UserService"]}, {"file": "service_25a9f3c7.ts", "missing": ["DeliveryService"]}, {"file": "service_80557028.ts", "missing": ["DeliveryService"]}, {"file": "service_57482eb6.ts", "missing": ["AuthService"]}, {"file": "service_89f4af1d.ts", "missing": ["EditorProjectService"]}, {"file": "service_352f2e0d.ts", "missing": ["RealizationTimeService"]}, {"file": "service_b1d447cb.ts", "missing": ["CurrencyRootService"]}, {"file": "service_710019a9.ts", "missing": ["LangRootService"]}, {"file": "service_07c088e3.ts", "missing": ["AuthService"]}, {"file": "LogoutService.ts", "missing": ["TokenService", "AuthService"]}, {"file": "editorprojectservice.ts", "missing": ["EditorProjectService"]}, {"file": "service_5d7129a2.ts", "missing": ["UserService"]}, {"file": "commonservice.ts", "missing": ["CommonService"]}, {"file": "service_12c3bdba.ts", "missing": ["DpCartsDataService"]}, {"file": "service_29e6e72f.ts", "missing": ["UserService"]}, {"file": "service_93b9c6cb.ts", "missing": ["DpProductService"]}, {"file": "OrderMessages.ts", "missing": ["TemplateRootService"]}, {"file": "service_8f2a392b.ts", "missing": ["DpCategoryService"]}, {"file": "service_7aba3a37.ts", "missing": ["DpCategoryService"]}, {"file": "addressservice.ts", "missing": ["AddressService"]}, {"file": "service_2585e686.ts", "missing": ["AuthService"]}, {"file": "service_1c53800c.ts", "missing": ["AddressService"]}, {"file": "delivery.ts", "missing": ["DeliveryService"]}, {"file": "service_ebd5cbb9.ts", "missing": ["DynamicCssService"]}, {"file": "service_dd582b42.ts", "missing": ["DpCategoryService"]}, {"file": "service_0e5426a2.ts", "missing": ["DeliveryService"]}, {"file": "service_ad249631.ts", "missing": ["CurrencyRootService", "CacheService"]}, {"file": "service_9fa8b6a6.ts", "missing": ["AddressService"]}, {"file": "service_a55d743e.ts", "missing": ["AuthService"]}, {"file": "service_bdcd6c40.ts", "missing": ["LangSettingsService"]}, {"file": "service_3de97a4e.ts", "missing": ["DeliveryService"]}, {"file": "service_eb2f7e64.ts", "missing": ["DeliveryService"]}, {"file": "MyController.ts", "missing": ["DpOrderService", "DeliveryService", "AddressService"]}, {"file": "OrderProcessor.ts", "missing": ["CalculationService"]}, {"file": "service_6a2e49ab.ts", "missing": ["UserService"]}, {"file": "service_16a9faf0.ts", "missing": ["DeliveryService"]}, {"file": "pstooltipservice.ts", "missing": ["PsTooltipService"]}, {"file": "service_e585e785.ts", "missing": ["DeliveryService"]}, {"file": "cart.ts", "missing": ["CartService"]}, {"file": "authdataservice.ts", "missing": ["AuthService"]}, {"file": "service_8457dd1e.ts", "missing": ["DpCategoryService"]}, {"file": "CartWidgetService.ts", "missing": ["CalculateDataService", "DpCartsDataService", "CountService", "CalcSimplifyWidgetService", "MainWidgetService", "AuthService", "PsGroupService", "DeliveryService", "DpProductService", "CalculationService", "TemplateRootService", "DeliveryWidgetService"]}, {"file": "calculation.ts", "missing": ["CalculationService"]}, {"file": "service_ba2cc373.ts", "missing": ["RegisterWidget"]}, {"file": "service_4d4bbcb4.ts", "missing": ["DeliveryService"]}, {"file": "service_f0119ca0.ts", "missing": ["DeliveryWidgetService"]}, {"file": "service_f7fbf1e1.ts", "missing": ["DpCartsDataService"]}, {"file": "service_80e377d4.ts", "missing": ["DeliveryService"]}, {"file": "service_54755db6.ts", "missing": ["DeliveryService"]}, {"file": "service_fa4ce491.ts", "missing": ["DpProductService"]}, {"file": "service_cfa64448.ts", "missing": ["AuthService"]}, {"file": "service_0d818615.ts", "missing": ["CalculationService"]}, {"file": "service_cf29c48d.ts", "missing": ["DpOrderService", "DeliveryService"]}, {"file": "SocialWidgetService.ts", "missing": ["AuthService"]}, {"file": "service_1be12164.ts", "missing": ["DeliveryService"]}, {"file": "LangService.ts", "missing": ["CacheService"]}, {"file": "auth.ts", "missing": ["AuthService"]}, {"file": "service_40c17f26.ts", "missing": ["CalculationService"]}, {"file": "address.ts", "missing": ["AddressService"]}, {"file": "service_a93b3a7f.ts", "missing": ["EditorProjectService"]}, {"file": "service_d7dcc341.ts", "missing": ["EditorProjectService"]}, {"file": "service_dbc259af.ts", "missing": ["UserService"]}, {"file": "service_5c2943b0.ts", "missing": ["DeliveryService"]}, {"file": "PsGroupService.ts", "missing": ["CacheService"]}, {"file": "service_a23d01fd.ts", "missing": ["DpProductService"]}, {"file": "DynamicCSS.ts", "missing": ["DynamicCssService"]}, {"file": "service_1b097db6.ts", "missing": ["AddressService"]}, {"file": "service_edb641f3.ts", "missing": ["AuthService"]}, {"file": "service_46639810.ts", "missing": ["PsAttributeService"]}, {"file": "user.ts", "missing": ["UserService"]}, {"file": "service_38d556d0.ts", "missing": ["DeliveryService"]}, {"file": "deliveryservice.ts", "missing": ["DeliveryService"]}, {"file": "service_087a7d19.ts", "missing": ["LangRootService"]}, {"file": "instead.ts", "missing": ["TokenService"]}, {"file": "service_c41d6c92.ts", "missing": ["RealizationTimeService"]}, {"file": "service_67f541ea.ts", "missing": ["AddressService"]}, {"file": "service_2815b72e.ts", "missing": ["CartService"]}, {"file": "service_17af4b1f.ts", "missing": ["LangSettingsService"]}, {"file": "setting.ts", "missing": ["SettingService"]}, {"file": "service_d8738c1f.ts", "missing": ["CurrencyRootService"]}, {"file": "service_43b08655.ts", "missing": ["RealizationTimeService"]}, {"file": "service_10e7dcdf.ts", "missing": ["RealizationTimeService"]}, {"file": "service_5bb8aae9.ts", "missing": ["DeliveryService"]}, {"file": "service_43c1ec4e.ts", "missing": ["DpCartsDataService"]}]}
"""

def apply_fixes():
    data = json.loads(REPORT_JSON)
    services_path = Path("/home/operator/dreamsoft_factory/next-frontend/src/services")
    
    print(f"🚀 Applying {len(data['fixes_required'])} import fixes...")
    
    updated_count = 0
    for fix in data["fixes_required"]:
        file_path = services_path / fix["file"]
        if not file_path.exists():
            # Try case-insensitive or common variants
            matches = list(services_path.glob(f"{fix['file'].lower()}"))
            if matches:
                file_path = matches[0]
            else:
                print(f"   ⚠️ File not found: {fix['file']}")
                continue
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Heuristic: Find first line after potential existing imports or at top
        import_lines = []
        for missing_service in fix["missing"]:
            # Check if already has some form of this import
            if any(f"import {{ {missing_service} }}" in line or f"import {missing_service} " in line for line in lines):
                continue
            
            # Simple assumption: all services are in the same folder for now
            import_lines.append(f"import {missing_service} from './{missing_service}';\n")
        
        if import_lines:
            new_content = "".join(import_lines) + "".join(lines)
            with open(file_path, 'w') as f:
                f.write(new_content)
            updated_count += 1
            if updated_count % 20 == 0:
                print(f"   Fixed {updated_count} files...")

    print(f"✅ Finished. Total files patched: {updated_count}")

if __name__ == "__main__":
    apply_fixes()
