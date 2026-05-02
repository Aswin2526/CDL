import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import {
  selectAuth,
  updateUserProfile,
  clearError,
} from '../../redux/auth/authSlice'
import { fetchProfile } from '../../services/authService'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import { ROUTES, resolveMediaUrl } from '../../utils/constants'

function formatMemberSince(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-NP', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

function getInitials(name) {
  if (!name) return '?'
  return name
    .split(/\s+/)
    .filter(Boolean)
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase()
}

function CustomerHome() {
  const dispatch = useDispatch()
  const { user, loading, error } = useSelector(selectAuth)
  const [profile, setProfile] = useState(null)
  const [profileLoading, setProfileLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [saveMsg, setSaveMsg] = useState('')
  const [form, setForm] = useState({
    full_name: '',
    phone_number: '',
    address: '',
  })

  useEffect(() => {
    let active = true
    setProfileLoading(true)
    fetchProfile()
      .then(({ data }) => {
        if (!active) return
        setProfile(data)
        setForm({
          full_name: data.full_name || '',
          phone_number: data.phone_number || '',
          address: data.customer_profile?.address || '',
        })
      })
      .catch(() => {
        if (active && user) {
          setProfile(user)
          setForm({
            full_name: user.full_name || '',
            phone_number: user.phone_number || '',
            address: user.customer_profile?.address || '',
          })
        }
      })
      .finally(() => {
        if (active) setProfileLoading(false)
      })
    return () => {
      active = false
    }
  }, [user])

  const display = profile || user
  const avatarUrl = display?.profile_image
    ? resolveMediaUrl(display.profile_image)
    : null

  const handleSave = async (e) => {
    e.preventDefault()
    setSaveMsg('')
    dispatch(clearError())
    const result = await dispatch(updateUserProfile(form))
    if (updateUserProfile.fulfilled.match(result)) {
      setProfile(result.payload)
      setEditing(false)
      setSaveMsg('Profile updated successfully.')
    }
  }

  const handleCancel = () => {
    setEditing(false)
    setSaveMsg('')
    dispatch(clearError())
    if (display) {
      setForm({
        full_name: display.full_name || '',
        phone_number: display.phone_number || '',
        address: display.customer_profile?.address || '',
      })
    }
  }

  if (profileLoading && !display) {
    return (
      <section className="mx-auto max-w-7xl px-4 py-12">
        <LoadingSpinner />
      </section>
    )
  }

  return (
    <section className="mx-auto max-w-7xl px-4 py-8 md:py-12">
      <h1 className="text-2xl font-bold text-gray-900 md:text-3xl">My account</h1>
      <p className="mt-1 text-gray-500">Your collector profile on ChitraBazar</p>

      <div className="mt-8 grid gap-8 lg:grid-cols-3">
        <div className="rounded-xl border border-stone-200 bg-white p-6 shadow-sm lg:col-span-1">
          <div className="flex flex-col items-center text-center">
            {avatarUrl ? (
              <img
                src={avatarUrl}
                alt=""
                className="h-24 w-24 rounded-full border-2 border-amber-100 object-cover"
              />
            ) : (
              <div className="flex h-24 w-24 items-center justify-center rounded-full bg-amber-100 text-2xl font-bold text-amber-900">
                {getInitials(display?.full_name)}
              </div>
            )}
            <h2 className="mt-4 text-xl font-semibold text-gray-900">
              {display?.full_name || 'Collector'}
            </h2>
            <p className="mt-1 text-sm text-gray-500">{display?.email}</p>
            <span className="mt-3 rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-900">
              {display?.role === 'admin' ? 'Administrator' : 'Art collector'}
            </span>
          </div>

          <dl className="mt-8 space-y-3 border-t border-stone-100 pt-6 text-sm">
            <div className="flex justify-between gap-4">
              <dt className="text-gray-500">Member since</dt>
              <dd className="font-medium text-gray-900">
                {formatMemberSince(display?.created_at)}
              </dd>
            </div>
            <div className="flex justify-between gap-4">
              <dt className="text-gray-500">Phone</dt>
              <dd className="text-right font-medium text-gray-900">
                {display?.phone_number || '—'}
              </dd>
            </div>
          </dl>
        </div>

        <div className="space-y-6 lg:col-span-2">
          <div className="rounded-xl border border-stone-200 bg-white p-6 shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h3 className="text-lg font-semibold text-gray-900">Profile information</h3>
              {!editing && (
                <button
                  type="button"
                  onClick={() => setEditing(true)}
                  className="rounded-lg border border-amber-600 px-4 py-1.5 text-sm font-medium text-amber-800 hover:bg-amber-50"
                >
                  Edit profile
                </button>
              )}
            </div>

            {!editing ? (
              <dl className="mt-6 grid gap-4 sm:grid-cols-2">
                <div>
                  <dt className="text-sm text-gray-500">Full name</dt>
                  <dd className="mt-1 font-medium text-gray-900">
                    {display?.full_name || '—'}
                  </dd>
                </div>
                <div>
                  <dt className="text-sm text-gray-500">Email</dt>
                  <dd className="mt-1 font-medium text-gray-900">{display?.email}</dd>
                </div>
                <div>
                  <dt className="text-sm text-gray-500">Phone number</dt>
                  <dd className="mt-1 font-medium text-gray-900">
                    {display?.phone_number || '—'}
                  </dd>
                </div>
                <div className="sm:col-span-2">
                  <dt className="text-sm text-gray-500">Delivery address</dt>
                  <dd className="mt-1 font-medium text-gray-900 whitespace-pre-line">
                    {display?.customer_profile?.address || 'Not added yet'}
                  </dd>
                </div>
              </dl>
            ) : (
              <form onSubmit={handleSave} className="mt-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Full name
                  </label>
                  <input
                    type="text"
                    required
                    value={form.full_name}
                    onChange={(e) => setForm((f) => ({ ...f, full_name: e.target.value }))}
                    className="mt-1 w-full rounded-lg border border-stone-300 px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Phone number
                  </label>
                  <input
                    type="tel"
                    value={form.phone_number}
                    onChange={(e) =>
                      setForm((f) => ({ ...f, phone_number: e.target.value }))
                    }
                    placeholder="98XXXXXXXX"
                    className="mt-1 w-full rounded-lg border border-stone-300 px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Delivery address
                  </label>
                  <textarea
                    rows={3}
                    value={form.address}
                    onChange={(e) => setForm((f) => ({ ...f, address: e.target.value }))}
                    placeholder="City, street, ward — for painting delivery"
                    className="mt-1 w-full rounded-lg border border-stone-300 px-3 py-2 text-sm"
                  />
                </div>
                {error && (
                  <p className="text-sm text-red-600">
                    {error.detail ||
                      (typeof error === 'object'
                        ? Object.values(error).flat().join(' ')
                        : 'Update failed')}
                  </p>
                )}
                <div className="flex gap-3">
                  <button
                    type="submit"
                    disabled={loading}
                    className="rounded-lg bg-amber-600 px-5 py-2 text-sm font-semibold text-white hover:bg-amber-700 disabled:opacity-60"
                  >
                    {loading ? 'Saving…' : 'Save changes'}
                  </button>
                  <button
                    type="button"
                    onClick={handleCancel}
                    className="rounded-lg border border-stone-300 px-5 py-2 text-sm font-medium text-gray-700 hover:bg-stone-50"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            )}

            {saveMsg && !editing && (
              <p className="mt-4 text-sm text-amber-800">{saveMsg}</p>
            )}
          </div>

          <div className="rounded-xl border border-stone-200 bg-stone-50 p-6">
            <h3 className="text-lg font-semibold text-gray-900">Quick links</h3>
            <div className="mt-4 flex flex-wrap gap-3">
              <Link
                to={ROUTES.SHOP}
                className="rounded-lg bg-amber-600 px-4 py-2 text-sm font-medium text-white hover:bg-amber-700"
              >
                Browse gallery
              </Link>
              <Link
                to={ROUTES.WISHLIST}
                className="rounded-lg border border-stone-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:border-amber-500"
              >
                Saved artworks
              </Link>
              <Link
                to={ROUTES.CART}
                className="rounded-lg border border-stone-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:border-amber-500"
              >
                View cart
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default CustomerHome
