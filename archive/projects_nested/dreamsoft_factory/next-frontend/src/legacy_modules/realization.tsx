/**
 * Service: realization
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const RealizationComponent: React.FC<RealizationProps> = ({ realisationTime, currentLang, loadVolumes }) => {
    return (
        <div>
            <span className="realization-time-label">
                {realisationTime.names[currentLang.code]}
            </span>
            <span className="shipping-time">
                <span className="text">{'delivery_send' | translate}</span>
                <span className="date" data-testid={!realisationTime.overwriteDate ? 'realisation-date' : undefined}>
                    {realisationTime.date}
                </span>
                <span className="text-danger date" data-testid={realisationTime.overwriteDate ? 'overwrite-date' : undefined}>
                    {realisationTime.overwriteDate}
                </span>
            </span>
            <span className="info">
                {'price' | translate} netto/{{'gross' | translate}}
            </span>
            <table data-testid="volume-table" hidden={loadVolumes}>
                <thead>
                    <th>{'volume' | translate}</th>
                    {realisationTimes.map((rt, index) => (
                        <th key={index} className="th-realisation-time">
                            <span className="realization-time-label">
                                {rt.names[currentLang.code]}
                            </span>
                            <span className="shipping-time">
                                <span className="text">{'delivery_send' | translate}</span>
                                <span className="date" data-testid={!rt.overwriteDate ? 'realisation-date' : undefined}>
                                    {rt.date}
                                </span>
                                <span className="text-danger date" data-testid={rt.overwriteDate ? 'overwrite-date' : undefined}>
                                    {rt.overwriteDate}
                                </span>
                            </span>
                            <span className="info">
                                {'price' | translate} netto/{{'gross' | translate}}
                            </span>
                        </th>
                    ))}
                </thead>
                <tbody>
                    {volumes.length > 1 ? (
                        volumes.map((volume, volIndex) => (
                            <tr key={volIndex} id={`row-volume-${volume.volume}`}>
                                <td className="col-volume">
                                    <span className="volume-icon">
                                        <img loading="lazy" className="price-list-icon" alt="" src={volume.calculation.priceListIcon.url} />
                                    </span>
                                    <span className="fa fa-pencil text-info custom-volume" data-testid={volume.custom ? 'custom-volume' : undefined}>
                                        {volume.volume}
                                    </span>
                                </td>
                                {realisationTimes.map((rt, rtIndex) => (
                                    <td key={rtIndex}>
                                        <div className="col-box-volume" data-testid={`col-box-${rt.ID}`}>
                                            {(rtVolume.volume === activeVolume.volume && activeVolume.rtID === rt.ID) ? 'bg-success' : ''}
                                            {rtVolume.volume === volume.volume && rtVolume.active && (
                                                <span ngClass={rtVolume.oldPrice ? 'price-special' : 'price-regular'}>
                                                    <span className="price-net">{rtVolume.price | priceFilter} {currentCurrency.symbol}</span>
                                                    <br />
                                                    <span className="price-gross">{rtVolume.priceBrutto} {currentCurrency.symbol}</span>
                                                </span>
                                            )}
                                        </div>
                                    </td>
                                ))}
                            </tr>
                        ))
                    ) : (
                        <tr data-testid="one-line-price">
                            <td className="col-volume">
                                <span className="volume-icon">
                                    <img loading="lazy" className="price-list-icon" alt="" src={volume.calculation.priceListIcon.url} />
                                </span>
                                <span className="fa fa-pencil text-info custom-volume" data-testid={volume.custom ? 'custom-volume' : undefined}>
                                    {volume.volume}
                                </span>
                            </td>
                            {realisationTimes.map((rt, rtIndex) => (
                                <td key={rtIndex}>
                                    <div className="col-box-volume" data-testid={`col-box-${rt.ID}`}>
                                        {(rtVolume.volume === activeVolume.volume && activeVolume.rtID === rt.ID) ? 'bg-success' : ''}
                                        {rtVolume.volume === volume.volume && rtVolume.active && (
                                            <span ngClass={rtVolume.oldPrice ? 'price-special' : 'price-regular'}>
                                                <span className="price-net">{rtVolume.price | priceFilter} {currentCurrency.symbol}</span>
                                                <br />
                                                <span className="price-gross">{rtVolume.priceBrutto} {currentCurrency.symbol}</span>
                                            </span>
                                        )}
                                    </div>
                                </td>
                            ))}
                        </tr>
                    )}
                </tbody>
            </table>
            <div className="loading text-center text-primary" data-testid="loading-spinner" hidden={!loadVolumes}>
                <i className="fa fa-spinner fa-pulse fa-fw"></i>
                <span>{'please_wait' | translate}</span>
            </div>
        </div>
    );
};

export default RealizationComponent;