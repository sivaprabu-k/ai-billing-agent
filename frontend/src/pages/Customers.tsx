import { useState } from "react";
import CustomerStats from "../components/dashboard/CustomerStats";
import CustomerToolbar from "../components/dashboard/CustomerToolbar";
import CustomerTable from "../components/dashboard/CustomerTable";
import AddCustomerModal from "../components/dashboard/AddCustomerModal";

import type { Customer } from "../types/customer";

const initialCustomers: Customer[] = [
  {
    id: "CUS-1001",
    name: "John Smith",
    email: "john@example.com",
    plan: "Professional",
    joined: "Jan 12, 2026",
    spent: "$1,250.00",
    status: "Active",
  },
  {
    id: "CUS-1002",
    name: "Sarah Johnson",
    email: "sarah@example.com",
    plan: "Basic",
    joined: "Feb 05, 2026",
    spent: "$450.00",
    status: "Active",
  },
  {
    id: "CUS-1003",
    name: "Michael Brown",
    email: "michael@example.com",
    plan: "Enterprise",
    joined: "Mar 18, 2026",
    spent: "$3,200.00",
    status: "Active",
  },
  {
    id: "CUS-1004",
    name: "Emily Davis",
    email: "emily@example.com",
    plan: "Professional",
    joined: "Apr 22, 2026",
    spent: "$980.00",
    status: "Inactive",
  },
  {
    id: "CUS-1005",
    name: "David Wilson",
    email: "david@example.com",
    plan: "Basic",
    joined: "May 10, 2026",
    spent: "$320.00",
    status: "Active",
  },
];

function Customers() {
  const [customers, setCustomers] = useState<Customer[]>(initialCustomers);

  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(
    null,
  );

  const [formError, setFormError] = useState("");

  const handleOpenAddModal = () => {
    setSelectedCustomer(null);
    setFormError("");
    setIsModalOpen(true);
  };

  const handleEditCustomer = (customer: Customer) => {
    setSelectedCustomer(customer);
    setFormError("");
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedCustomer(null);
    setFormError("");
  };

  const handleDeleteCustomer = (customerId: string) => {
    setCustomers((prev) =>
      prev.filter((customer) => customer.id !== customerId),
    );
  };

  const handleAddCustomer = (customerData: {
    name: string;
    email: string;
    plan: string;
  }) => {
    const emailExists = customers.some(
      (customer) =>
        customer.email.toLowerCase() === customerData.email.toLowerCase(),
    );

    if (emailExists) {
      setFormError("A customer with this email already exists.");
      return;
    }

    const highestId = customers.reduce((max, customer) => {
      const numericId = Number(customer.id.replace("CUS-", ""));
      return Math.max(max, numericId);
    }, 1000);

    const newCustomer: Customer = {
      id: `CUS-${highestId + 1}`,
      name: customerData.name,
      email: customerData.email,
      plan: customerData.plan,
      joined: new Date().toLocaleDateString("en-US", {
        month: "short",
        day: "2-digit",
        year: "numeric",
      }),
      spent: "$0.00",
      status: "Active",
    };

    setCustomers((prev) => [...prev, newCustomer]);
    handleCloseModal();
  };

  const handleUpdateCustomer = (customerData: {
    name: string;
    email: string;
    plan: string;
  }) => {
    if (!selectedCustomer) return;

    const emailExists = customers.some(
      (customer) =>
        customer.id !== selectedCustomer.id &&
        customer.email.toLowerCase() === customerData.email.toLowerCase(),
    );

    if (emailExists) {
      setFormError("Another customer is already using this email.");
      return;
    }

    setCustomers((prev) =>
      prev.map((customer) =>
        customer.id === selectedCustomer.id
          ? {
              ...customer,
              name: customerData.name,
              email: customerData.email,
              plan: customerData.plan,
            }
          : customer,
      ),
    );

    handleCloseModal();
  };

  const handleCustomerSubmit = (customerData: {
    name: string;
    email: string;
    plan: string;
  }) => {
    if (selectedCustomer) {
      handleUpdateCustomer(customerData);
    } else {
      handleAddCustomer(customerData);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-2xl font-bold text-white">Customers</h1>
          <p className="mt-1 text-sm text-gray-400">
            Manage your customers and subscription details.
          </p>
        </div>

        <button
          type="button"
          onClick={handleOpenAddModal}
          className="rounded-lg bg-purple-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-purple-500"
        >
          Add Customer
        </button>
      </div>

      <CustomerStats />

      <CustomerToolbar
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        statusFilter={statusFilter}
        onStatusChange={setStatusFilter}
      />

      <CustomerTable
        customers={customers}
        searchTerm={searchTerm}
        statusFilter={statusFilter}
        onEditCustomer={handleEditCustomer}
        onDeleteCustomer={handleDeleteCustomer}
      />

      {isModalOpen && (
        <AddCustomerModal
          onClose={handleCloseModal}
          onSubmit={handleCustomerSubmit}
          error={formError}
          customer={selectedCustomer}
        />
      )}
    </div>
  );
}

export default Customers;
