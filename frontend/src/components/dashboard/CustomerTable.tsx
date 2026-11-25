import { useEffect, useState } from "react";
import {
  Eye,
  MoreHorizontal,
  Pencil,
  Trash2,
  X,
  AlertTriangle,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import type { Customer } from "../../types/customer";

interface CustomerTableProps {
  customers: Customer[];
  searchTerm: string;
  statusFilter: string;
  onEditCustomer: (customer: Customer) => void;
  onDeleteCustomer: (customerId: string) => void;
}

function CustomerTable({
  customers,
  searchTerm,
  statusFilter,
  onEditCustomer,
  onDeleteCustomer,
}: CustomerTableProps) {
  const [openMenuId, setOpenMenuId] = useState<string | null>(null);
  const [selectedCustomer, setSelectedCustomer] =
    useState<Customer | null>(null);
  const [customerToDelete, setCustomerToDelete] =
    useState<Customer | null>(null);

  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(5);

  const filteredCustomers = customers.filter((customer) => {
    const search = searchTerm.toLowerCase();

    const matchesSearch =
      customer.name.toLowerCase().includes(search) ||
      customer.email.toLowerCase().includes(search) ||
      customer.id.toLowerCase().includes(search);

    const matchesStatus =
      statusFilter === "All" || customer.status === statusFilter;

    return matchesSearch && matchesStatus;
  });

  const totalCustomers = filteredCustomers.length;
  const totalPages = Math.ceil(totalCustomers / itemsPerPage);

  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;

  const currentCustomers = filteredCustomers.slice(startIndex, endIndex);

  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, statusFilter, itemsPerPage]);

  useEffect(() => {
    if (totalPages === 0 && currentPage !== 1) {
      setCurrentPage(1);
    } else if (totalPages > 0 && currentPage > totalPages) {
      setCurrentPage(totalPages);
    }
  }, [totalPages, currentPage]);

  const closeDetails = () => setSelectedCustomer(null);

  const handleDelete = () => {
    if (!customerToDelete) return;

    onDeleteCustomer(customerToDelete.id);
    setCustomerToDelete(null);
  };

  const handlePreviousPage = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 1));
  };

  const handleNextPage = () => {
    setCurrentPage((prev) => Math.min(prev + 1, totalPages));
  };

  return (
    <>
      <div className="overflow-hidden rounded-xl border border-white/10 bg-[#15151f]">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[900px] text-left">
            <thead className="border-b border-white/10 bg-white/[0.03]">
              <tr className="text-sm text-gray-400">
                <th className="px-6 py-4 font-medium">Customer</th>
                <th className="px-6 py-4 font-medium">Customer ID</th>
                <th className="px-6 py-4 font-medium">Plan</th>
                <th className="px-6 py-4 font-medium">Joined Date</th>
                <th className="px-6 py-4 font-medium">Total Spent</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 text-right font-medium">Action</th>
              </tr>
            </thead>

            <tbody className="divide-y divide-white/5">
              {currentCustomers.length > 0 ? (
                currentCustomers.map((customer) => (
                  <tr
                    key={customer.id}
                    className="transition-colors hover:bg-white/[0.02]"
                  >
                    <td className="px-6 py-4">
                      <div>
                        <p className="font-medium text-white">
                          {customer.name}
                        </p>
                        <p className="mt-1 text-sm text-gray-400">
                          {customer.email}
                        </p>
                      </div>
                    </td>

                    <td className="px-6 py-4 text-sm text-gray-400">
                      {customer.id}
                    </td>

                    <td className="px-6 py-4 text-sm text-gray-300">
                      {customer.plan}
                    </td>

                    <td className="px-6 py-4 text-sm text-gray-400">
                      {customer.joined}
                    </td>

                    <td className="px-6 py-4 text-sm text-gray-300">
                      {customer.spent}
                    </td>

                    <td className="px-6 py-4">
                      <span
                        className={`rounded-full px-3 py-1 text-xs font-medium ${
                          customer.status === "Active"
                            ? "bg-green-500/10 text-green-400"
                            : "bg-red-500/10 text-red-400"
                        }`}
                      >
                        {customer.status}
                      </span>
                    </td>

                    <td className="px-6 py-4 text-right">
                      <div className="relative inline-block">
                        <button
                          type="button"
                          onClick={() =>
                            setOpenMenuId(
                              openMenuId === customer.id ? null : customer.id,
                            )
                          }
                          className="rounded-lg p-2 text-gray-400 transition hover:bg-white/10 hover:text-white"
                          aria-label={`Actions for ${customer.name}`}
                        >
                          <MoreHorizontal size={20} />
                        </button>

                        {openMenuId === customer.id && (
                          <div className="absolute right-0 z-20 mt-2 w-48 rounded-lg border border-white/10 bg-[#20202c] p-1 shadow-xl">
                            <button
                              type="button"
                              onClick={() => {
                                setSelectedCustomer(customer);
                                setOpenMenuId(null);
                              }}
                              className="flex w-full items-center gap-3 rounded-md px-3 py-2.5 text-left text-sm text-gray-300 transition hover:bg-white/10 hover:text-white"
                            >
                              <Eye size={16} />
                              View Details
                            </button>

                            <button
                              type="button"
                              onClick={() => {
                                onEditCustomer(customer);
                                setOpenMenuId(null);
                              }}
                              className="flex w-full items-center gap-3 rounded-md px-3 py-2.5 text-left text-sm text-gray-300 transition hover:bg-white/10 hover:text-white"
                            >
                              <Pencil size={16} />
                              Edit Customer
                            </button>

                            <button
                              type="button"
                              onClick={() => {
                                setCustomerToDelete(customer);
                                setOpenMenuId(null);
                              }}
                              className="flex w-full items-center gap-3 rounded-md px-3 py-2.5 text-left text-sm text-red-400 transition hover:bg-red-500/10"
                            >
                              <Trash2 size={16} />
                              Delete Customer
                            </button>
                          </div>
                        )}
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan={7}
                    className="px-6 py-12 text-center text-sm text-gray-400"
                  >
                    No customers found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="flex flex-col gap-4 border-t border-white/10 px-6 py-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-sm text-gray-400">
              Rows per page
            </span>

            <select
              value={itemsPerPage}
              onChange={(event) =>
                setItemsPerPage(Number(event.target.value))
              }
              className="rounded-lg border border-white/10 bg-[#20202c] px-3 py-2 text-sm text-white outline-none focus:border-purple-500"
              aria-label="Rows per page"
            >
              <option value={5}>5</option>
              <option value={10}>10</option>
              <option value={20}>20</option>
            </select>

            <span className="text-sm text-gray-400">
              {totalCustomers === 0
                ? "Showing 0 customers"
                : `Showing ${startIndex + 1}-${Math.min(
                    endIndex,
                    totalCustomers,
                  )} of ${totalCustomers} customers`}
            </span>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-400">
              Page {totalPages === 0 ? 0 : currentPage} of {totalPages}
            </span>

            <button
              type="button"
              onClick={handlePreviousPage}
              disabled={currentPage === 1 || totalPages === 0}
              className="rounded-lg border border-white/10 p-2 text-gray-300 transition hover:bg-white/10 hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
              aria-label="Previous page"
            >
              <ChevronLeft size={18} />
            </button>

            <button
              type="button"
              onClick={handleNextPage}
              disabled={currentPage >= totalPages || totalPages === 0}
              className="rounded-lg border border-white/10 p-2 text-gray-300 transition hover:bg-white/10 hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
              aria-label="Next page"
            >
              <ChevronRight size={18} />
            </button>
          </div>
        </div>
      </div>

      {selectedCustomer && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">
          <div className="w-full max-w-lg rounded-2xl border border-white/10 bg-[#181824] p-6 shadow-2xl">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold text-white">
                  Customer Details
                </h2>
                <p className="mt-1 text-sm text-gray-400">
                  Customer information and account summary.
                </p>
              </div>

              <button
                type="button"
                onClick={closeDetails}
                className="rounded-lg p-2 text-gray-400 transition hover:bg-white/10 hover:text-white"
                aria-label="Close customer details"
              >
                <X size={20} />
              </button>
            </div>

            <div className="space-y-5">
              <div>
                <p className="text-sm text-gray-400">Customer Name</p>
                <p className="mt-1 font-medium text-white">
                  {selectedCustomer.name}
                </p>
              </div>

              <div>
                <p className="text-sm text-gray-400">Email Address</p>
                <p className="mt-1 text-white">{selectedCustomer.email}</p>
              </div>

              <div className="grid grid-cols-2 gap-5">
                <div>
                  <p className="text-sm text-gray-400">Customer ID</p>
                  <p className="mt-1 text-white">{selectedCustomer.id}</p>
                </div>

                <div>
                  <p className="text-sm text-gray-400">Subscription Plan</p>
                  <p className="mt-1 text-white">{selectedCustomer.plan}</p>
                </div>

                <div>
                  <p className="text-sm text-gray-400">Joined Date</p>
                  <p className="mt-1 text-white">{selectedCustomer.joined}</p>
                </div>

                <div>
                  <p className="text-sm text-gray-400">Total Spent</p>
                  <p className="mt-1 text-white">{selectedCustomer.spent}</p>
                </div>
              </div>

              <div>
                <p className="text-sm text-gray-400">Account Status</p>
                <span
                  className={`mt-2 inline-flex rounded-full px-3 py-1 text-xs font-medium ${
                    selectedCustomer.status === "Active"
                      ? "bg-green-500/10 text-green-400"
                      : "bg-red-500/10 text-red-400"
                  }`}
                >
                  {selectedCustomer.status}
                </span>
              </div>
            </div>

            <div className="mt-8 flex justify-end">
              <button
                type="button"
                onClick={closeDetails}
                className="rounded-lg border border-white/10 px-5 py-2.5 text-sm font-medium text-gray-300 transition hover:bg-white/5 hover:text-white"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {customerToDelete && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm">
          <div
            role="alertdialog"
            aria-modal="true"
            aria-labelledby="delete-customer-title"
            className="w-full max-w-md rounded-2xl border border-[#343440] bg-[#131319] p-7 shadow-2xl"
          >
            <div className="mb-5 flex items-center gap-4">
              <div className="rounded-xl bg-red-500/10 p-3 text-red-400">
                <AlertTriangle size={24} />
              </div>

              <div>
                <h2
                  id="delete-customer-title"
                  className="text-lg font-semibold text-white"
                >
                  Delete Customer
                </h2>
                <p className="mt-1 text-sm text-zinc-500">
                  This action cannot be undone.
                </p>
              </div>
            </div>

            <p className="mb-2 text-sm text-zinc-300">
              Are you sure you want to delete this customer?
            </p>

            <div className="mb-6 rounded-lg border border-white/10 bg-white/[0.03] px-4 py-3">
              <p className="font-medium text-white">
                {customerToDelete.name}
              </p>
              <p className="mt-1 text-sm text-zinc-400">
                {customerToDelete.id}
              </p>
              <p className="mt-1 text-sm text-zinc-500">
                {customerToDelete.email}
              </p>
            </div>

            <div className="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
              <button
                type="button"
                onClick={() => setCustomerToDelete(null)}
                className="rounded-xl border border-[#343440] px-5 py-3 text-sm font-medium text-zinc-300 transition hover:bg-[#272731]"
              >
                Cancel
              </button>

              <button
                type="button"
                onClick={handleDelete}
                className="rounded-xl bg-red-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-red-500"
              >
                Delete Customer
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default CustomerTable;
