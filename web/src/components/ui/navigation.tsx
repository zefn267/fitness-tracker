import Link from "next/link";
import { useRouter } from "next/router";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Home,
  Dumbbell,
  TrendingUp,
  User,
  Plus
} from "lucide-react";

const Navigation = () => {
  const router = useRouter();

  const navItems = [
    { path: "/", icon: Home, label: "Dashboard" },
    { path: "/workouts", icon: Dumbbell, label: "Workouts" },
    { path: "/progress", icon: TrendingUp, label: "Progress" },
    { path: "/profile", icon: User, label: "Profile" },
  ];

  return (
      <nav className="bg-card border-b border-border sticky top-0 z-50 backdrop-blur-sm bg-card/95">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-8">
              <Link href="/" className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center">
                  <Dumbbell className="h-5 w-5 text-primary-foreground" />
                </div>
                <span className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                FitTracker
              </span>
              </Link>

              <div className="flex items-center space-x-1">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  const isActive = router.pathname === item.path;

                  return (
                      <Link key={item.path} href={item.path}>
                        <Button
                            variant={isActive ? "default" : "ghost"}
                            size="sm"
                            className={cn(
                                "flex items-center space-x-2 transition-all duration-200",
                                isActive && "bg-primary text-primary-foreground shadow-lg"
                            )}
                        >
                          <Icon className="h-4 w-4" />
                          <span className="hidden md:inline">{item.label}</span>
                        </Button>
                      </Link>
                  );
                })}
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <Link href="/workouts/new">
                <Button className="flex items-center space-x-2 bg-gradient-to-r from-primary to-accent hover:opacity-90 transition-opacity">
                  <Plus className="h-4 w-4" />
                  <span className="hidden sm:inline">New Workout</span>
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>
  );
};

export default Navigation;