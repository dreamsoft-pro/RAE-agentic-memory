import api from '@/lib/api';

class DeviceService {
    private static speedUnits: Record<string, string> = {
        sheet: 'ark',
        squareMeter: 'm2',
        perimeter: 'mb',
        set: 'szt',
        projectSheets: 'ark',
        every_sheet_separate: 'ark',
        collectingFolds: 'falce',
        folds: 'falce'
    };

    public static async getSpeedUnit(unit: string): Promise<string> {
        if (DeviceService.speedUnits[unit]) {
            return DeviceService.speedUnits[unit];
        }
        return 'unit';
    }

    // You might want to add other methods or properties here as needed
}

export default DeviceService;