// src/components/Sidebar.jsx
import React, { useState } from "react";
import "../styles/Sidebar.css";

function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className={`sidebar ${collapsed ? "collapsed" : ""}`}>
      <button className="collapse-btn" onClick={() => setCollapsed(!collapsed)}>
        {collapsed ? "☰" : "<"}
      </button>

      {!collapsed && (
        <>
          <div className="sidebar-title">History</div>
          <ul className="sidebar-list">
            <li>
              <strong>Query</strong>
              <div className="timestamp">2h ago</div>
            </li>
          </ul>
        </>
      )}
    </div>
  );
}

export default Sidebar;
