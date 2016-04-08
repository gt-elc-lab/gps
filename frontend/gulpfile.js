var gulp = require('gulp');
var connect = require('gulp-connect');
var browserify = require('browserify');
var source = require('vinyl-source-stream');
var shell = require('gulp-shell');

gulp.task('connect', function () {
    connect.server({
        root: 'build',
        port: 4000
    });
});

gulp.task('admin_connect', function () {
    connect.server({
        root: 'admin_build',
        port: 4000
    });
});

gulp.task('watch', function() {
    gulp.watch('app/**/*.js', ['browserify_app']);
});

gulp.task('admin_watch', function() {
    gulp.watch('admin/**/*.js', ['browserify_admin']);
});

gulp.task('browserify_app', function() {
    // Grabs the app.js file
    return browserify('./app/app.js')
        // bundles it and creates a file called app.js
        .bundle()
        .pipe(source('app.js'))
        // saves it the build/js/ directory
        .pipe(gulp.dest('./build/js/'));
});

gulp.task('browserify_admin', function() {
    // Grabs the app.js file
    return browserify('./admin/admin.js')
        // bundles it and creates a file called app.js
        .bundle()
        .pipe(source('admin.js'))
        // saves it the build/js/ directory
        .pipe(gulp.dest('./admin_build/js/'));
});

gulp.task('default', ['connect', 'watch']);
gulp.task('admin', ['admin_connect', 'admin_watch']);