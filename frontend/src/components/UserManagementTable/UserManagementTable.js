import React, { useState, useRef } from 'react';
import { connect } from "react-redux"
import { useToasts } from "../../hooks/ui/useToasts" 
import { Actions as authActions } from "../../redux/auth"
// import { createDataStore } from '../data_store';
import {
  EuiButton,
  EuiSpacer,
  EuiBasicTable,
  EuiFlexGroup,
  EuiFlexItem,
  EuiModal,
  EuiModalBody,
  EuiModalHeader,
  EuiModalHeaderTitle,
  EuiModalFooter,
  EuiSuperSelect,
} from "@elastic/eui"
import validation from "../../utils/validation"
import styled from "styled-components"
import { extractErrorMessages } from "../../utils/errors"

const UserManagementTableWrapper = styled.div`
  padding: 2rem;
`
function UserManagementTable({ authError, isLoading, data, retrieveUsers, updateUserRole, switchUserDisabled}) {

    const { addToast } = useToasts()

    //api call to populate user list
    const populateUserList  = async () => {
        const res = await retrieveUsers()
        if (res.success){
            setUsers(res.data)
        }
    }

    const [pageIndex, setPageIndex] = useState(0)
    const [pageSize, setPageSize] = useState(5)
    const [sortField, setSortField] = useState('username')
    const [sortDirection, setSortDirection] = useState('asc')
    const [selectedItems, setSelectedItems] = useState([])
    const [users, setUsers] = useState ([])
    const [reload, setReload] = useState(false)
    const [selectedRole, setSelectedRole] = useState("")
    const [updateRole, setUpdateRole] = useState(false)
    const tableRef = useRef();

    const refreshTable = () =>{
        setSelectedItems([])
        setUpdateRole(false)
        tableRef.current.setSelection([])
        setReload(true)
    }

    const submitUpdateRole = async () => {
        //updateRole code here
        if(!selectedRole){
            addToast({
                id: `no-role-selected`,
                title: "No role selected",
                color: "warning",
                icontype: "alert",
                toastLifeTimeMs: 10000,
                text: "Please select a role from the drop-down box",
            })
            return
        }
        const selectedUser = selectedItems[0]
        const email = selectedUser.email
        const role = selectedRole
        const res = await updateUserRole({email: email, role: role})
        if(res.success){
            addToast({
                id: `role-changed-successfully`,
                title: "Role changed successfully",
                color: "success",
                icontype: "alert",
                toastLifeTimeMs: 15000,
            })
        }
        setSelectedRole("")
        refreshTable()
    }

    //when reload is true, populate user list
    React.useEffect(() => {
        if(reload === true){
            populateUserList()
            setReload(false)
        }
    }, [reload])

    //populate user list at render
    React.useEffect(() => {
        setReload(true)
    }, []) // <-- empty array means 'run once'

    const onTableChange = ({ page = {}, sort = {} }) => {
      const { index: pageIndex, size: pageSize } = page;
      const { field: sortField, direction: sortDirection } = sort;
  
      setPageIndex(pageIndex);
      setPageSize(pageSize);
      setSortField(sortField);
      setSortDirection(sortDirection);
    };
  
    const onSelectionChange = (selectedItems) => {
      setSelectedItems(selectedItems);
    };
  
    const onClickSwitchDisable = async () => {
      //delete users code here
      if (selectedItems.length === 0) {
        return;
      }
      if (selectedItems.length > 1){
        addToast({
            id: `auth-toast-toomany`,
            title: `Too many users selected`,
            color: "warning",
            iconType: "alert",
            toastLifeTimeMs: 15000,
            })
        return;
      }
      const selectedUser = selectedItems[0]
      const email = selectedUser.email
      const res = await switchUserDisabled({email: email})
      if(res.success){
        addToast({
          id: `switch-disabled-success`,
          title: "Success",
          color: "success",
          iconType: "alert",
          toastLifeTimeMs: 15000,
          text: "User status changed successfully"
        })
      }
      refreshTable()
    };
  
    const renderDisableButton = () => {
      if (selectedItems.length === 0) {
        return;
      }
      if (selectedItems.length > 1){
        return;
      }
      const selectedUser = selectedItems[0]
      var buttonstring = ""
      if(selectedUser.disabled){
        buttonstring = "Enable User"
      }
      else{
        buttonstring = "Disable User"
      }
      return (
        <EuiButton color="danger" isLoading={isLoading} onClick={() => {onClickSwitchDisable();}}>
            {buttonstring}
        </EuiButton>
      );
    };

    const closeDisplayModal = () => {
        setUpdateRole(false)
    }

    const changeUserRole = () => {
        if (selectedItems.length === 0) {
            return;
        }
        if (selectedItems.length > 1){
            addToast({
                id: `auth-toast-toomany`,
                title: `Too many users selected`,
                color: "Warning",
                iconType: "alert",
                toastLifeTimeMs: 15000,
              })
            return;
        }
        setUpdateRole(true)
    }

    const renderDisplayModal = () => {
        if(updateRole === true){
            return (         
                <EuiModal style={{ width: '800px' }} onClose= {() => {closeDisplayModal();}}>
                <EuiModalHeader>
                  <EuiModalHeaderTitle>
                    <h1>Change User Role</h1>
                  </EuiModalHeaderTitle>
                </EuiModalHeader>
                <EuiModalBody>
                  <p>
                    Select a role to change to:
                  </p>
                <EuiSpacer size="s" />
                <EuiSuperSelect
                    options={[
                    {
                        value: 'ADMIN',
                        inputDisplay: 'Admin'
                    },
                    {
                        value: 'USER',
                        inputDisplay: 'User'
                    },
                    {
                        value: 'GUEST',
                        inputDisplay: 'Guest'
                    },
                    ]}
                    valueOfSelected = {selectedRole}
                    onChange={(value) => setSelectedRole(value)}
                    itemLayoutAlign="top"
                />
                </EuiModalBody>
                
                <EuiModalFooter>
                <EuiButton onClick= {() => {submitUpdateRole();}} fill>
                    Submit
                </EuiButton>
                <EuiButton onClick= {() => {closeDisplayModal();}} fill>
                    Close
                </EuiButton>
                </EuiModalFooter>
              </EuiModal>
            )
        }
        else{
            return;
        }
    }
  
    // const { pageOfItems, totalItemCount } = store.findUsers(
    //   pageIndex,
    //   pageSize,
    //   sortField,
    //   sortDirection
    // );
  
    const disablebutton = renderDisableButton();
    const displayModal = renderDisplayModal();

  
    const columns = [
      {
        field: 'email',
        name: 'Email',
        sortable: true,
        truncateText: true,
        mobileOptions: {
          show: false,
        },
      },
      {
        field: 'username',
        name: 'Username',
        truncateText: true,
        mobileOptions: {
          show: false,
        },
      },
      {
        field: 'role',
        name: 'Role',
        mobileOptions: {
            show: false,
        },
      },
      {
        field: 'disabled',
        name: 'Disabled',
        mobileOptions: {
            show: false,
        }
      },
      {
        field: 'email_verified',
        name: 'Email Verified',
        mobileOptions: {
            show: false,
        }
      }
    ];
  
    const pagination = {
      pageIndex: pageIndex,
      pageSize: pageSize,
      totalItemCount: users.length,
      pageSizeOptions: [3, 5, 8],
    };
  
    const sorting = {
      sort: {
        field: sortField,
        direction: sortDirection,
      },
    };
  
    const selection = {
      onSelectionChange: onSelectionChange
    };
  

  return (
    <UserManagementTableWrapper>
     {displayModal}
      <EuiFlexGroup alignItems="center">
        <EuiFlexItem grow={false}>
          <EuiButton onClick={() => { changeUserRole(); }}>Change User Role</EuiButton>
        </EuiFlexItem>
        <EuiFlexItem />
        {disablebutton}
      </EuiFlexGroup>
      <EuiSpacer size="l" />
      <EuiBasicTable
        tableCaption="UserManagementTable"
        ref={tableRef}
        items={users}
        itemId="id"
        columns={columns}
        pagination={pagination}
        sorting={sorting}
        isSelectable={true}
        selection={selection}
        onChange={onTableChange}
        rowHeader="email"
      />
    </UserManagementTableWrapper>
  )
}

export default connect(
  (state) => ({
    authError: state.auth.error,
    isLoading: state.auth.isLoading,
    data: state.auth.data,
    user: state.auth.user,
  }),
  {
    retrieveUsers: authActions.retrieveUsers,
    updateUserRole: authActions.updateUserRole,
    switchUserDisabled: authActions.switchDisableUser
  }
)(UserManagementTable)


