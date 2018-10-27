import React from "react";
import { MenuItem, connectMenu, ContextMenu } from "react-contextmenu";
import ComponentStyle from "../scss/ContextMenu.scss";

const MENU_TYPE = "DYNAMIC";

const DynamicMenu = props => {
  const { id, trigger } = props;
  const handleItemClick = trigger ? trigger.onItemClick : null;

  return (
    <ContextMenu id={id} className={ComponentStyle.contextmenu}>
      {trigger && (
        <MenuItem
          className={ComponentStyle.contextmenu_item}
          onClick={handleItemClick}
          data={{ action: "Open" }}
        >
          Otwórz
        </MenuItem>
      )}
      {trigger && (
        <MenuItem
          className={ComponentStyle.contextmenu_item}
          onClick={handleItemClick}
          data={{ action: "Properties" }}
        >
          Właściwości
        </MenuItem>
      )}
      {trigger && (
        <MenuItem
          className={ComponentStyle.contextmenu_item}
          onClick={handleItemClick}
          data={{ action: "Delete" }}
        >
          Usuń
        </MenuItem>
      )}
    </ContextMenu>
  );
};

const ConnectedMenu = connectMenu(MENU_TYPE)(DynamicMenu);

export default ConnectedMenu;
