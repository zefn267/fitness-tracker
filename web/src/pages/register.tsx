import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Dumbbell, Eye, EyeOff } from 'lucide-react'
import { useDebounce } from 'use-debounce'
import { apiFetch } from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Separator } from '@/components/ui/separator'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { toast } from "sonner";
import { useRouter } from "next/router";

const registerSchema = z.object({
    username: z.string().min(3, 'Логин должен быть не менее 3 символов'),
    firstname: z.string().min(2, 'Имя должно быть минимум из 2 букв'),
    age: z.coerce.number().int().min(8, 'Minimum age is 8').max(100),
    gender: z.enum(['Мужской', 'Женский'], { required_error: 'Выберите Ваш пол' }),
    email: z.string().email('Неверный формат почты'),
    password: z.string().min(8, 'Пароль должен быть не менее 8 символов'),
    confirmPassword: z.string(),
}).refine(d => d.password === d.confirmPassword, {
    message: "Passwords don't match",
    path: ['confirmPassword'],
})

type RegisterFormData = z.infer<typeof registerSchema>

export default function RegisterPage() {
    const router = useRouter()
    const [showPassword, setShowPassword] = useState(false)
    const [showConfirmPassword, setShowConfirmPassword] = useState(false)
    const [isLoading, setIsLoading] = useState(false)

    const form = useForm<RegisterFormData>({
        resolver: zodResolver(registerSchema),
        defaultValues: {
            username: '',
            firstname: '',
            age: 18,
            gender: 'Мужской',
            email: '',
            password: '',
            confirmPassword: '',
        },
    })

    const username = form.watch('username')
    const [debouncedUsername] = useDebounce(username, 500)
    useEffect(() => {
        let active = true
        if (debouncedUsername && debouncedUsername.length >= 3) {
            fetch(`/api/auth/username?username=${encodeURIComponent(debouncedUsername)}`)
                .then(res => res.json())
                .then(data => {
                    if (!active) return
                    if (!data?.available) {
                        form.setError('username', { type: 'manual', message: 'This username is taken' })
                    } else {
                        if (form.getFieldState('username').error?.type === 'manual') {
                            form.clearErrors('username')
                        }
                    }
                })
                .catch(() => {
                    if (!active) return
                    form.setError('username', { type: 'manual', message: 'Error checking username' })
                })
        }
        return () => { active = false }
    }, [debouncedUsername, form])

    async function onSubmit(values: RegisterFormData) {
        setIsLoading(true)
        try {
            await apiFetch('/auth/register', {
                method: 'POST',
                body: JSON.stringify({
                    user_name: values.username,
                    first_name: values.firstname,
                    age: values.age,
                    gender: values.gender,
                    email: values.email,
                    password: values.password,
                }),
            })
            toast.success('Регистрация успешна!')
            router.push('/login')
        } catch (e: any) {
            console.error('register error:', e?.message)
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-background via-background to-accent/5 flex items-center justify-center p-4">
            <div className="w-full max-w-md">
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-gradient-to-br from-primary to-accent rounded-full flex items-center justify-center mx-auto mb-4">
                        <Dumbbell className="h-8 w-8 text-primary-foreground" />
                    </div>
                    <h1 className="text-3xl font-bold text-foreground mb-2">Добро пожаловать!</h1>
                    <p className="text-muted-foreground">Присоединяйтесь и начинайте отслеживать свой прогресс в тренировках</p>
                </div>

                <Card className="shadow-xl border-0 bg-card/95 backdrop-blur-sm">
                    <CardHeader className="space-y-1 pb-6">
                        <CardTitle className="text-2xl text-center">Регистрация</CardTitle>
                        <CardDescription className="text-center">Создайте свою учетную запись, чтобы начать</CardDescription>
                    </CardHeader>

                    <CardContent>
                        <Form {...form}>
                            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                                <div className="grid grid-cols-2 gap-4">
                                    <FormField
                                        control={form.control}
                                        name="username"
                                        render={({ field }) => (
                                            <FormItem>
                                                <FormLabel htmlFor={field.name}>Логин</FormLabel>
                                                <FormControl>
                                                    <Input
                                                        {...field}
                                                        id={field.name}
                                                        name={field.name}
                                                        autoComplete="username"
                                                        placeholder="john123"
                                                        className="h-11"
                                                    />
                                                </FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )}
                                    />

                                    <FormField
                                        control={form.control}
                                        name="firstname"
                                        render={({ field }) => (
                                            <FormItem>
                                                <FormLabel htmlFor={field.name}>Имя</FormLabel>
                                                <FormControl>
                                                    <Input
                                                        {...field}
                                                        id={field.name}
                                                        name={field.name}
                                                        autoComplete="given-name"
                                                        placeholder="John"
                                                        className="h-11"
                                                    />
                                                </FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )}
                                    />
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <FormField
                                        control={form.control}
                                        name="age"
                                        render={({ field }) => (
                                            <FormItem>
                                                <FormLabel htmlFor="age">Возраст</FormLabel>
                                                <FormControl>
                                                    <Select
                                                        value={field.value ? String(field.value) : ''}
                                                        onValueChange={(v) => field.onChange(Number(v))}
                                                    >
                                                        <SelectTrigger id="age" className="h-11">
                                                            <SelectValue placeholder="Select age" />
                                                        </SelectTrigger>
                                                        <SelectContent className="max-h-60">
                                                            {Array.from({ length: 100 - 8 + 1 }, (_, i) => 8 + i).map((n) => (
                                                                <SelectItem key={n} value={String(n)}>{n}</SelectItem>
                                                            ))}
                                                        </SelectContent>
                                                    </Select>
                                                </FormControl>
                                                <input type="hidden" name="age" id="age-hidden" value={field.value ?? ''} />
                                                <FormMessage />
                                            </FormItem>
                                        )}
                                    />

                                    <FormField
                                        control={form.control}
                                        name="gender"
                                        render={({ field }) => (
                                            <FormItem>
                                                <FormLabel htmlFor="gender">Пол</FormLabel>
                                                <FormControl>
                                                    <Select value={field.value} onValueChange={field.onChange}>
                                                        <SelectTrigger id="gender" className="h-11">
                                                            <SelectValue placeholder="Select gender" />
                                                        </SelectTrigger>
                                                        <SelectContent>
                                                            <SelectItem value="Мужской">Мужской</SelectItem>
                                                            <SelectItem value="Женский">Женский</SelectItem>
                                                        </SelectContent>
                                                    </Select>
                                                </FormControl>
                                                <input type="hidden" name="gender" id="gender-hidden" value={field.value ?? ''} />
                                                <FormMessage />
                                            </FormItem>
                                        )}
                                    />
                                </div>

                                <FormField
                                    control={form.control}
                                    name="email"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel htmlFor={field.name}>Почта</FormLabel>
                                            <FormControl>
                                                <Input
                                                    {...field}
                                                    id={field.name}
                                                    name={field.name}
                                                    autoComplete="email"
                                                    type="email"
                                                    placeholder="john.doe@example.com"
                                                    className="h-11"
                                                />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                <FormField
                                    control={form.control}
                                    name="password"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel htmlFor={field.name}>Пароль</FormLabel>
                                            <FormControl>
                                                <div className="relative">
                                                    <Input
                                                        {...field}
                                                        id={field.name}
                                                        name={field.name}
                                                        autoComplete="new-password"
                                                        type={showPassword ? 'text' : 'password'}
                                                        placeholder="Create a strong password"
                                                        className="h-11 pr-10"
                                                    />
                                                    <Button
                                                        type="button"
                                                        variant="ghost"
                                                        size="sm"
                                                        className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                                                        onClick={() => setShowPassword(v => !v)}
                                                    >
                                                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                                    </Button>
                                                </div>
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                <FormField
                                    control={form.control}
                                    name="confirmPassword"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel htmlFor={field.name}>Подтверждение пароля</FormLabel>
                                            <FormControl>
                                                <div className="relative">
                                                    <Input
                                                        {...field}
                                                        id={field.name}
                                                        name={field.name}
                                                        autoComplete="new-password"
                                                        type={showConfirmPassword ? 'text' : 'password'}
                                                        placeholder="Confirm your password"
                                                        className="h-11 pr-10"
                                                    />
                                                    <Button
                                                        type="button"
                                                        variant="ghost"
                                                        size="sm"
                                                        className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                                                        onClick={() => setShowConfirmPassword(v => !v)}
                                                    >
                                                        {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                                    </Button>
                                                </div>
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                {/* Terms */}
                                <div className="text-center text-sm leading-relaxed text-muted-foreground">
                                    Создавая аккаунт, вы соглашаетесь с{' '}
                                    <Link href="/terms" className="text-primary hover:underline">
                                        Пользовательским соглашением
                                    </Link>{' '}
                                    и{' '}
                                    <Link href="/privacy" className="text-primary hover:underline">
                                        Политикой конфиденциальности
                                    </Link>.
                                </div>

                                <Button
                                    type="submit"
                                    className="w-full h-11 bg-gradient-to-r from-primary to-accent hover:opacity-90 transition-opacity"
                                    disabled={isLoading}
                                >
                                    {isLoading ? 'Создание аккаунта...' : 'Создать аккаунт'}
                                </Button>
                            </form>
                        </Form>

                        <Separator className="my-6" />
                        <div className="text-center text-sm">
                            <span className="text-muted-foreground">Уже есть аккаунт? </span>
                            <Link href="/login" className="text-primary hover:text-primary/80 transition-colors font-medium">
                                Вход
                            </Link>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
