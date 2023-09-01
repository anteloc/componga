cmake_minimum_required(VERSION 3.10)

project(Componga_project VERSION $ENV{APPVEYOR_BUILD_VERSION} LANGUAGES NONE)

add_executable(componga-windows IMPORTED)

set_property(TARGET componga-windows PROPERTY
             IMPORTED_LOCATION "dist/componga-windows/componga-windows.exe")

# Specify the install rules for the files in componga-windows directory
install(DIRECTORY ./ DESTINATION ./)

set(CPACK_GENERATOR "WIX")

# Name in Applications and Features (Windows Settings)
set(CPACK_PACKAGE_NAME "Componga")

# Name for the installer, without extension
set(CPACK_PACKAGE_FILE_NAME "componga-$ENV{APPVEYOR_BUILD_VERSION}-windows")

set(CPACK_PACKAGE_VENDOR "anteloc")
set(CPACK_PACKAGE_DESCRIPTION "Componga Application")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Componga: a screen annotation tool for presentations")

# Add-Remove-Programs comment
set(CPACK_WIX_PROPERTY_ARPCOMMENTS "Screen annotation tool")

# Install directory name under X:\Program Files (x86)
set(CPACK_PACKAGE_INSTALL_DIRECTORY "Componga")

set(CPACK_WIX_UPGRADE_GUID "87F9D9CA-9654-4DC7-8BE6-8CD923CD0028")
set(CPACK_WIX_UNINSTALL "1")

# Support non-interactive sessions (like CI).
set(CPACK_WIX_LIGHT_EXTRA_FLAGS "-sval")

set(CPACK_PACKAGE_EXECUTABLES "componga-windows;Componga")

set(CPACK_CREATE_DESKTOP_LINKS "componga-windows")

set(CPACK_RESOURCE_FILE_LICENSE "dist/componga-windows/LICENSE.txt")

set(CPACK_PACKAGE_VERSION $ENV{APPVEYOR_BUILD_VERSION})

set(CPACK_WIX_PROGRAM_MENU_FOLDER "Componga Screen Annotation Tool")

include(CPack)
