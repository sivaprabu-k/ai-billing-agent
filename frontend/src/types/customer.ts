export interface Customer {
  id: string;
  name: string;
  email: string;
  plan: string;
  joined: string;
  spent: string;
  status: "Active" | "Inactive";
}