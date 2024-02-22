/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { UiShellLeftPanel } from "../UiShellLeftPanel";
import "./style.css";

export const NavigationSideNav = ({ version, className }) => {
  return (
    <div className={`navigation-side-nav ${version} ${className}`}>
      <div className="frame-2">
        {version === "version-4" && (
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider={false}
            expanded={false}
            level="level-1"
            linkIconClassName="UI-shell-left-panel-instance"
            linkText="My experiments"
            selected={false}
            stateProp="enabled"
            type="link"
          />
        )}

        <div className="frame-3">
          {["v1", "version-4"].includes(version) && (
            <div className="frame-4">
              {version === "version-4" && (
                <UiShellLeftPanel
                  className="UI-shell-left-panel-menu-item"
                  compact={false}
                  divider={false}
                  expanded={false}
                  level="level-1"
                  linkIconClassName="UI-shell-left-panel-instance"
                  linkText="Workflows"
                  selected={false}
                  stateProp="enabled"
                  type="link"
                />
              )}

              {version === "v1" && (
                <>
                  <UiShellLeftPanel
                    className="UI-shell-left-panel-menu-item"
                    compact={false}
                    divider={false}
                    expanded={false}
                    level="level-1"
                    linkText="My experiments"
                    selected={false}
                    stateProp="enabled"
                    type="link"
                  />
                  <UiShellLeftPanel
                    className="UI-shell-left-panel-menu-item"
                    compact={false}
                    divider={false}
                    expanded={false}
                    level="level-2"
                    linkText="All"
                    selected
                    stateProp="selected"
                    type="link"
                  />
                  <UiShellLeftPanel
                    className="UI-shell-left-panel-menu-item"
                    compact={false}
                    divider={false}
                    expanded={false}
                    level="level-2"
                    linkText="In progress"
                    selected={false}
                    stateProp="enabled"
                    type="link"
                  />
                  <UiShellLeftPanel
                    className="UI-shell-left-panel-menu-item"
                    compact={false}
                    divider={false}
                    expanded={false}
                    level="level-2"
                    linkText="With error"
                    selected={false}
                    stateProp="enabled"
                    type="link"
                  />
                  <UiShellLeftPanel
                    className="UI-shell-left-panel-menu-item"
                    compact={false}
                    divider={false}
                    expanded={false}
                    level="level-2"
                    linkText="Complete"
                    selected={false}
                    stateProp="enabled"
                    type="link"
                  />
                  <UiShellLeftPanel
                    className="UI-shell-left-panel-menu-item"
                    compact={false}
                    divider={false}
                    expanded={false}
                    level="level-2"
                    linkText="Archived"
                    selected={false}
                    stateProp="enabled"
                    type="link"
                  />
                </>
              )}
            </div>
          )}

          {["v2", "v3", "version-5"].includes(version) && (
            <>
              <UiShellLeftPanel
                className="UI-shell-left-panel-menu-item"
                compact={false}
                divider={false}
                expanded={false}
                level="level-1"
                linkText="My experiments"
                selected={false}
                stateProp="enabled"
                type="link"
              />
              <UiShellLeftPanel
                className="UI-shell-left-panel-menu-item"
                compact={false}
                divider={false}
                expanded={false}
                level="level-2"
                linkText="All"
                selected
                stateProp="selected"
                type="link"
              />
              <UiShellLeftPanel
                className="UI-shell-left-panel-menu-item"
                compact={false}
                divider={false}
                expanded={false}
                level="level-2"
                linkText="In progress"
                selected={false}
                stateProp="enabled"
                type="link"
              />
              <UiShellLeftPanel
                className="UI-shell-left-panel-menu-item"
                compact={false}
                divider={false}
                expanded={false}
                level="level-2"
                linkText={version === "version-5" ? "With error" : "Error"}
                selected={false}
                stateProp="enabled"
                type="link"
              />
              <UiShellLeftPanel
                className="UI-shell-left-panel-menu-item"
                compact={false}
                divider={false}
                expanded={false}
                level="level-2"
                linkText="Complete"
                selected={false}
                stateProp="enabled"
                type="link"
              />
              <UiShellLeftPanel
                className="UI-shell-left-panel-menu-item"
                compact={false}
                divider={false}
                expanded={false}
                level="level-2"
                linkText="Archived"
                selected={false}
                stateProp="enabled"
                type="link"
              />
            </>
          )}
        </div>
        {version === "version-4" && (
          <>
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider={false}
              expanded={false}
              level="level-2"
              linkIconClassName="UI-shell-left-panel-menu-item-instance"
              linkText="In progress"
              selected={false}
              stateProp="enabled"
              type="link"
            />
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider={false}
              expanded={false}
              level="level-2"
              linkIconClassName="UI-shell-left-panel-menu-item-instance"
              linkText="With error"
              selected={false}
              stateProp="enabled"
              type="link"
            />
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider={false}
              expanded={false}
              level="level-2"
              linkIconClassName="UI-shell-left-panel-menu-item-instance"
              linkText="Complete"
              selected={false}
              stateProp="enabled"
              type="link"
            />
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider={false}
              expanded={false}
              level="level-2"
              linkIconClassName="UI-shell-left-panel-menu-item-instance"
              linkText="Archived"
              selected={false}
              stateProp="enabled"
              type="link"
            />
          </>
        )}

        {version === "v3" && (
          <UiShellLeftPanel
            className="UI-shell-left-panel-menu-item"
            compact={false}
            divider
            expanded={false}
            level="level-1"
            selected={false}
            stateProp="enabled"
            type="divider"
          />
        )}

        {["v1", "v3"].includes(version) && (
          <div className="frame-5">
            {version === "v1" && (
              <div className="UI-shell-left-panel-wrapper">
                <UiShellLeftPanel
                  className="UI-shell-left-panel-menu-item"
                  compact={false}
                  divider={false}
                  expanded={false}
                  level="level-1"
                  linkText="Workflows"
                  selected={false}
                  stateProp="enabled"
                  type="link"
                />
              </div>
            )}

            {version === "v3" && (
              <>
                <UiShellLeftPanel
                  className="UI-shell-left-panel-menu-item"
                  compact={false}
                  divider={false}
                  expanded={false}
                  level="level-1"
                  linkText="Wild types"
                  selected={false}
                  stateProp="enabled"
                  type="link"
                />
                <UiShellLeftPanel
                  className="UI-shell-left-panel-menu-item"
                  compact={false}
                  divider={false}
                  expanded={false}
                  level="level-1"
                  linkText="Parameter files"
                  selected={false}
                  stateProp="enabled"
                  type="link"
                />
                <UiShellLeftPanel
                  className="UI-shell-left-panel-menu-item"
                  compact={false}
                  divider={false}
                  expanded={false}
                  level="level-1"
                  linkText="Outputs"
                  selected={false}
                  stateProp="enabled"
                  type="link"
                />
              </>
            )}
          </div>
        )}

        {version === "v3" && (
          <>
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider
              expanded={false}
              level="level-1"
              selected={false}
              stateProp="enabled"
              type="divider"
            />
            <div className="frame-6">
              <UiShellLeftPanel
                className="UI-shell-left-panel-menu-item"
                compact={false}
                divider={false}
                expanded={false}
                level="level-1"
                linkText="Favourites"
                selected={false}
                stateProp="enabled"
                type="link"
              />
              <UiShellLeftPanel
                className="UI-shell-left-panel-menu-item"
                compact={false}
                divider={false}
                expanded={false}
                level="level-2"
                linkText="My favourited view 1"
                selected={false}
                stateProp="enabled"
                type="link"
              />
              <UiShellLeftPanel
                className="UI-shell-left-panel-menu-item"
                compact={false}
                divider={false}
                expanded={false}
                level="level-2"
                linkText="My favourited view 2"
                selected={false}
                stateProp="enabled"
                type="link"
              />
            </div>
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider
              expanded={false}
              level="level-1"
              selected={false}
              stateProp="enabled"
              type="divider"
            />
          </>
        )}
      </div>
      <div className="frame-7">
        {["v1", "v2", "v3", "version-4"].includes(version) && (
          <>
            <UiShellLeftPanel
              className={`${["v1", "version-4"].includes(version) ? "UI-shell-left-panel-menu-item" : "class"}`}
              compact={false}
              divider={false}
              expanded={false}
              level="level-1"
              linkIconClassName={`${version === "version-4" && "UI-shell-left-panel-instance"}`}
              linkText="Help"
              selected={false}
              stateProp="enabled"
              type="link"
            />
            <UiShellLeftPanel
              className={`${["v1", "version-4"].includes(version) ? "UI-shell-left-panel-menu-item" : "class"}`}
              compact={false}
              divider={false}
              expanded={false}
              level="level-1"
              linkIconClassName={`${version === "version-4" && "UI-shell-left-panel-instance"}`}
              linkText="Feedback"
              selected={false}
              stateProp="enabled"
              type="link"
            />
            <UiShellLeftPanel
              className={`${["v1", "version-4"].includes(version) ? "UI-shell-left-panel-menu-item" : "class"}`}
              compact={false}
              divider={false}
              expanded={false}
              level="level-1"
              linkIconClassName={`${version === "version-4" && "UI-shell-left-panel-instance"}`}
              linkText="Settings"
              selected={false}
              stateProp="enabled"
              type="link"
            />
          </>
        )}

        {version === "version-5" && (
          <div className="frame-8">
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider
              expanded={false}
              level="level-1"
              selected={false}
              stateProp="enabled"
              type="divider"
            />
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider={false}
              expanded={false}
              level="level-2"
              linkText="Example experiment 01"
              selected={false}
              stateProp="enabled"
              type="link"
            />
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider={false}
              expanded={false}
              level="level-2"
              linkText="Example experiment 02"
              selected={false}
              stateProp="enabled"
              type="link"
            />
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider={false}
              expanded={false}
              level="level-2"
              linkText="Example experiment 03"
              selected={false}
              stateProp="enabled"
              type="link"
            />
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider={false}
              expanded={false}
              level="level-2"
              linkText="Example experiment 04"
              selected={false}
              stateProp="enabled"
              type="link"
            />
            <UiShellLeftPanel
              className="UI-shell-left-panel-menu-item"
              compact={false}
              divider={false}
              expanded={false}
              level="level-2"
              linkText="Example experiment 05"
              selected={false}
              stateProp="enabled"
              type="link"
            />
          </div>
        )}
      </div>
    </div>
  );
};

NavigationSideNav.propTypes = {
  version: PropTypes.oneOf(["v3", "v1", "version-5", "version-4", "v2"]),
};
