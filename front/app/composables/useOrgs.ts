import { useApi } from "./useAPI";

// frontend/app/composables/useOrgs.ts
export type License = { id:number; code:string; issued_at:string | null }
export type Org = {
  id:number; name:string; bin:string; logo:string | null;
  licenses: License[];
}

export const useOrgs = () => {
  const api = useApi()

  const listOrgs = async (q = "") => {
    const { data } = await api.get(`/orgs/${q ? `?${q}` : ""}`)
    return data
  }

  const getOrg = async (id: string | number) => {
    const { data } = await api.get(`/orgs/${id}/`)
    return data as Org
  }

  const listLicenses = async () => {
    const { data } = await api.get(`/licenses/?limit=1000`)
    return data
  }

  const createOrg = async (payload: FormData | object) => {
    const { data } = await api.post(`/orgs/`, payload)
    return data as Org
  }

  const updateOrg = async (id:number, payload: FormData | object) => {
    const { data } = await api.patch(`/orgs/${id}/`, payload)
    return data as Org
  }

  const deleteOrg = async (id:number) => {
    await api.delete(`/orgs/${id}/`)
  }

  return { listOrgs, getOrg, listLicenses, createOrg, updateOrg, deleteOrg }
}
