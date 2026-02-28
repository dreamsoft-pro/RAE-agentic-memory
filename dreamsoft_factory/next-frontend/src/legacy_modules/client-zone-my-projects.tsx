/**
 * Service: client-zone-my-projects
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Project {
    created: Date;
    updated: Date;
    projectName: string;
    inEditor: number;
    emailShared: boolean;
}

interface Props {
    projects: Project[];
    shareByEmail: (project: Project) => void;
    prepareUrl: (project: Project) => void;
    remove: (project: Project) => void;
    currentLang: { code: string };
    pagingSettings: { total: number };
    getNextPage: (page: number) => void;
    pageSizeSelect: number[];
    changeLimit: (limit: number) => void;
    sortBy: (field: keyof Project) => void;
}

const ClientZoneMyProjects: React.FC<Props> = ({ projects, shareByEmail, prepareUrl, remove, currentLang, pagingSettings, getNextPage, pageSizeSelect, changeLimit, sortBy }) => {
    return (
        <div className="panel panel-default">
            <div className="panel-heading">
                <h2 className="panel-title">{'my_projects' | translate}</h2>
            </div>
            <div className="panel-body">
                <div className="row">
                    <div className="col-md-12">
                        <ul className="nav nav-tabs">
                            {/* Existing tabs */}
                        </ul>
                    </div>
                </div>
                <div className="roundborder margintop">
                    <div className="panel">
                        <div className="table-responsive">
                            <table className="table table-hover">
                                <thead>
                                    <tr>
                                        <th></th>
                                        <th>{'create_date' | translate}</th>
                                        <th>{'update_date' | translate}</th>
                                        <th>{'name' | translate}</th>
                                        <th>{'product_name' | translate}</th>
                                        <th>{'status' | translate}</th>
                                        <th>{'actions' | translate}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {projects.map((project, index) => (
                                        <tr key={index}>
                                            <td>{index + 1}</td>
                                            <td><span>{project.created.toISOString().split('T')[0]}</span></td>
                                            <td><span>{project.updated.toISOString().replace('T', ' ').slice(0, -3)}</span></td>
                                            <td>{project.projectName}</td>
                                            <td>{project.projects[0].typeInfo.names[currentLang.code]}</td>
                                            <td>
                                                <i 
                                                    className={`fa ${project.inEditor === 1 ? 'text-danger' : project.inEditor === 2 ? 'text-success' : ''}`}
                                                    title={project.inEditor === 1 ? ('status_in_editor' | translate) : project.inEditor === 2 ? ('status_ordered' | translate) : ''}
                                                />
                                            </td>
                                            <td>
                                                <button onClick={() => shareByEmail(project)} title={'share_with_email' | translate} className="btn btn-xs btn-basic">
                                                    <i className="fa fa-envelope-o" aria-hidden="true"></i>
                                                </button>
                                                <button onClick={() => prepareUrl(project)} className="btn btn-xs btn-success">
                                                    <span className="fa fa-edit" aria-hidden="true"></span>
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ClientZoneMyProjects;