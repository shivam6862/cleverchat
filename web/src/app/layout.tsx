import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "@/styles/globals.css";
import Header from "@/components/Header/Header";
import Footer from "@/components/Footer/Footer";
import { NotificationContextProvider } from "@/contexts/NotificationContext";
import { AppContextProvider } from "@/contexts/AppContext";
import Notifications from "@/components/Notification/Notifications";
const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Genius Learning HubAi",
  description:
    "AI-driven app with smart navigation, interactive chatbot, insightful videos, and personalized assessments.",
  icons: ["robot.jpg"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <NotificationContextProvider>
          <AppContextProvider>
            <Notifications />
            <Header />
            {children}
            <Footer />
          </AppContextProvider>
        </NotificationContextProvider>
      </body>
    </html>
  );
}
