import { useState } from "react";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { Dumbbell, Eye, EyeOff, XCircle } from "lucide-react";
import { toast } from "sonner";
import { apiFetch } from "@/lib/api";

import {
    Card, CardContent, CardHeader, CardTitle, CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Form, FormControl, FormField, FormItem, FormLabel,
} from "@/components/ui/form";
import { Separator } from "@/components/ui/separator";

type LoginFormData = { username: string; password: string };

export default function Login() {
    const [showPassword, setShowPassword] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    // без resolver, без схемы — сами проверим пустые поля
    const form = useForm<LoginFormData>({
        defaultValues: { username: "", password: "" },
        mode: "onSubmit",
    });

    const onSubmit = async (data: LoginFormData) => {
        const missing: string[] = [];
        if (!data.username.trim()) missing.push("Поле Логин обязательно для заполнения.");
        if (!data.password.trim()) missing.push("Поле Пароль обязательно для заполнения.");

        if (missing.length) {
            toast.dismiss();
            if (missing.length === 2) {
                toast.error(
                    "Поле Логин обязательно для заполнения.\nПоле Пароль обязательно для заполнения.",
                    { icon: <XCircle className="h-5 w-5 text-red-500" /> }
                );
            } else {
                toast.error(missing[0], { icon: <XCircle className="h-5 w-5 text-red-500" /> });
            }
            return;
        }

        setIsLoading(true);
        try {
            await apiFetch("/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({
                    username: data.username,
                    password: data.password,
                }),
            });
            toast.success("Вы успешно вошли!");
            // router.push('/me')
        } catch (e: any) {
            toast.error("Неверный логин или пароль", {
                icon: <XCircle className="h-5 w-5 text-red-500" />,
            });
            form.resetField("password");
            console.error("login error:", e?.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-background via-background to-accent/5 flex items-center justify-center p-4">
            <div className="w-full max-w-md">
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-gradient-to-br from-primary to-accent rounded-full flex items-center justify-center mx-auto mb-4">
                        <Dumbbell className="h-8 w-8 text-primary-foreground" />
                    </div>
                    <h1 className="text-3xl font-bold text-foreground mb-2">С возвращением</h1>
                    <p className="text-muted-foreground">Войдите, чтобы продолжить</p>
                </div>

                <Card className="shadow-xl border-0 bg-card/95 backdrop-blur-sm">
                    <CardHeader className="space-y-1 pb-6">
                        <CardTitle className="text-2xl text-center">Вход</CardTitle>
                        <CardDescription className="text-center">
                            Введите свои данные для доступа к аккаунту
                        </CardDescription>
                    </CardHeader>

                    <CardContent>
                        <Form {...form}>
                            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                                {/* Логин — без FormMessage и без error-классов */}
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
                                                    type="text"
                                                    autoComplete="username"
                                                    placeholder="Введите логин"
                                                    className="h-11"
                                                />
                                            </FormControl>
                                        </FormItem>
                                    )}
                                />

                                {/* Пароль — без FormMessage и без error-классов */}
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
                                                        type={showPassword ? "text" : "password"}
                                                        autoComplete="current-password"
                                                        placeholder="Введите пароль"
                                                        className="h-11 pr-10"
                                                    />
                                                    <Button
                                                        type="button"
                                                        variant="ghost"
                                                        size="sm"
                                                        className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                                                        onClick={() => setShowPassword((v) => !v)}
                                                        aria-label={showPassword ? "Скрыть пароль" : "Показать пароль"}
                                                    >
                                                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                                    </Button>
                                                </div>
                                            </FormControl>
                                        </FormItem>
                                    )}
                                />

                                <div className="flex items-center justify-between">
                                    <div className="text-sm">
                                        <Link href="/forgot-password" className="text-primary hover:text-primary/80 transition-colors">
                                            Забыли пароль?
                                        </Link>
                                    </div>
                                </div>

                                <Button
                                    type="submit"
                                    className="w-full h-11 bg-gradient-to-r from-primary to-accent hover:opacity-90 transition-opacity"
                                    disabled={isLoading}
                                >
                                    {isLoading ? "Входим..." : "Войти"}
                                </Button>
                            </form>
                        </Form>

                        <Separator className="my-6" />
                        <div className="text-center text-sm">
                            <span className="text-muted-foreground">Нет аккаунта? </span>
                            <Link href="/register" className="text-primary hover:text-primary/80 transition-colors font-medium">
                                Зарегистрироваться
                            </Link>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
