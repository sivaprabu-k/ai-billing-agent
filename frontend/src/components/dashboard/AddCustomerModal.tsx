import { useState } from "react";
import { X } from "lucide-react";
import type { Customer } from "../../types/customer";

interface AddCustomerModalProps {
  onClose: () => void;
  onSubmit: (customer: {
    name: string;
    email: string;
    plan: string;
  }) => void;
  error: string;
  customer?: Customer | null;
}

function AddCustomerModal({
  onClose,
  onSubmit,
  error,
  customer,
}: AddCustomerModalProps) {
  const [name, setName] = useState(customer?.name ?? "");
  const [email, setEmail] = useState(customer?.email ?? "");
  const [plan, setPlan] = useState(customer?.plan ?? "Basic");

  const isEditMode = Boolean(customer);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (name.trim().length < 2) {
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      return;
    }

    onSubmit({
      name: name.trim(),
      email: email.trim().toLowerCase(),
      plan,
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-6 backdrop-blur-sm">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="customer-modal-title"
        className="w-full max-w-lg overflow-hidden rounded-2xl border border-[#343440] bg-[#131319] shadow-2xl"
      >
        {/* Header */}
        <div className="flex items-center justify-between border-b border-[#272731] px-8 py-7">
          <div>
            <h2
              id="customer-modal-title"
              className="text-xl font-semibold text-white"
            >
              {isEditMode ? "Edit Customer" : "Add Customer"}
            </h2>

            <p className="mt-2 text-sm text-zinc-500">
              {isEditMode
                ? "Update the customer's information."
                : "Enter the customer's information."}
            </p>
          </div>

          <button
            type="button"
            onClick={onClose}
            aria-label="Close modal"
            className="rounded-lg p-2.5 text-zinc-400 transition hover:bg-[#272731] hover:text-white"
          >
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-7 px-8 py-8">
          {isEditMode && customer && (
            <div className="rounded-xl border border-[#30303b] bg-[#0d0d11] px-4 py-3">
              <p className="text-xs font-medium text-zinc-500">
                Customer ID
              </p>
              <p className="mt-1 text-sm font-medium text-zinc-200">
                {customer.id}
              </p>
            </div>
          )}

          <div>
            <label
              htmlFor="customer-name"
              className="mb-3 block text-sm font-medium text-zinc-300"
            >
              Customer Name
            </label>

            <input
              id="customer-name"
              type="text"
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder="Enter customer name"
              className="w-full rounded-xl border border-[#30303b] bg-[#0d0d11] px-4 py-3.5 text-sm text-white outline-none transition placeholder:text-zinc-600 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/10"
              required
              minLength={2}
            />
          </div>

          <div>
            <label
              htmlFor="customer-email"
              className="mb-3 block text-sm font-medium text-zinc-300"
            >
              Email Address
            </label>

            <input
              id="customer-email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="Enter email address"
              className="w-full rounded-xl border border-[#30303b] bg-[#0d0d11] px-4 py-3.5 text-sm text-white outline-none transition placeholder:text-zinc-600 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/10"
              required
            />
          </div>

          <div>
            <label
              htmlFor="customer-plan"
              className="mb-3 block text-sm font-medium text-zinc-300"
            >
              Subscription Plan
            </label>

            <select
              id="customer-plan"
              value={plan}
              onChange={(event) => setPlan(event.target.value)}
              className="w-full rounded-xl border border-[#30303b] bg-[#0d0d11] px-4 py-3.5 text-sm text-white outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-500/10"
            >
              <option value="Basic">Basic</option>
              <option value="Professional">Professional</option>
              <option value="Enterprise">Enterprise</option>
            </select>
          </div>

          {error && (
            <p
              role="alert"
              className="rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400"
            >
              {error}
            </p>
          )}

          <div className="flex flex-col-reverse gap-3 border-t border-[#272731] pt-6 sm:flex-row sm:justify-end">
            <button
              type="button"
              onClick={onClose}
              className="rounded-xl border border-[#343440] px-6 py-3 text-sm font-medium text-zinc-300 transition hover:bg-[#272731]"
            >
              Cancel
            </button>

            <button
              type="submit"
              className="rounded-xl bg-purple-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-purple-500"
            >
              {isEditMode ? "Save Changes" : "Create Customer"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddCustomerModal;
