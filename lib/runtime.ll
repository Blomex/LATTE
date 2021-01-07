@dnl = internal constant [4 x i8] c"%d\0A\00"
@fnl = internal constant [6 x i8] c"%.1f\0A\00"
@lf  = internal constant [4 x i8] c"%lf\00"
@err = internal constant [14 x i8] c"runtime error\00"
@.str = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@stdin = external local_unnamed_addr constant %struct._IO_FILE*, align 8
@str = private unnamed_addr constant [14 x i8] c"Runtime error\00"
declare i32 @printf(i8*, ...)
declare i32 @strcmp(i8*, i8*)
declare i32 @scanf(i8*, ...)
declare i32 @puts(i8*)
declare i8* @malloc(i64)
declare void @free(i8*)
declare i8* @memcpy(i8*, i8*, i32)
%struct._IO_FILE = type opaque
declare void @llvm.lifetime.start.p0i8(i64, i8* nocapture) #2
declare i8* @strcpy(i8*, i8* nocapture readonly) local_unnamed_addr #1
declare void @exit(i32) local_unnamed_addr #6
declare i64 @strlen(i8* nocapture) local_unnamed_addr #4

declare i8* @strcat(i8*, i8* nocapture readonly) local_unnamed_addr #1
declare i64 @getline(i8**, i64*, %struct._IO_FILE*) local_unnamed_addr #3

; Function Attrs: argmemonly nounwind
declare void @llvm.lifetime.end.p0i8(i64, i8* nocapture) #2

attributes #0 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+sse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+sse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { argmemonly nounwind }
attributes #3 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+sse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { argmemonly nounwind readonly "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+sse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #5 = { noreturn nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+sse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #6 = { noreturn "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+sse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #7 = { nounwind }
attributes #8 = { noreturn nounwind }

define void @printInt(i32 %x) {
       %t0 = getelementptr [4 x i8], [4 x i8]* @dnl, i32 0, i32 0
       call i32 (i8*, ...) @printf(i8* %t0, i32 %x)
       ret void
}

define i8* @readString() local_unnamed_addr #0 {
  %1 = alloca i8*, align 8
  %2 = alloca i64, align 8
  %3 = bitcast i8** %1 to i8*
  call void @llvm.lifetime.start.p0i8(i64 8, i8* nonnull %3) #7
  store i8* null, i8** %1, align 8, !tbaa !2
  %4 = bitcast i64* %2 to i8*
  call void @llvm.lifetime.start.p0i8(i64 8, i8* nonnull %4) #7
  store i64 0, i64* %2, align 8, !tbaa !6
  %5 = load %struct._IO_FILE*, %struct._IO_FILE** @stdin, align 8, !tbaa !2
  %6 = call i64 @getline(i8** nonnull %1, i64* nonnull %2, %struct._IO_FILE* %5) #7
  %7 = icmp eq i64 %6, -1
  br i1 %7, label %8, label %9

; <label>:8:                                      ; preds = %0
  call void @error()
  unreachable

; <label>:9:                                      ; preds = %0
  %10 = load i8*, i8** %1, align 8, !tbaa !2
  %11 = add nsw i64 %6, -1
  %12 = getelementptr inbounds i8, i8* %10, i64 %11
  %13 = load i8, i8* %12, align 1, !tbaa !8
  %14 = icmp eq i8 %13, 10
  br i1 %14, label %15, label %17

; <label>:15:                                     ; preds = %9
  store i8 0, i8* %12, align 1, !tbaa !8
  %16 = load i8*, i8** %1, align 8, !tbaa !2
  br label %17

; <label>:17:                                     ; preds = %15, %9
  %18 = phi i8* [ %16, %15 ], [ %10, %9 ]
  call void @llvm.lifetime.end.p0i8(i64 8, i8* nonnull %4) #7
  call void @llvm.lifetime.end.p0i8(i64 8, i8* nonnull %3) #7
  ret i8* %18
}

define i32 @readInt() local_unnamed_addr {
  %1 = alloca i32, align 4
  %2 = bitcast i32* %1 to i8*
  call void @llvm.lifetime.start.p0i8(i64 4, i8* nonnull %2) #7
  %3 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i64 0, i64 0), i32* nonnull %1)
  %4 = icmp eq i32 %3, -1
  br i1 %4, label %5, label %6

; <label>:5:                                      ; preds = %0
  call void @error()
  unreachable

; <label>:6:                                      ; preds = %0
  %7 = load i32, i32* %1, align 4, !tbaa !9
  call void @llvm.lifetime.end.p0i8(i64 4, i8* nonnull %2) #7
  ret i32 %7
}

define void @error() local_unnamed_addr noreturn nounwind {
  %1 = tail call i32 @puts(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @str, i64 0, i64 0))
  tail call void @exit(i32 1) #8
  unreachable
}

define i8* @concat(i8* nocapture readonly, i8* nocapture readonly) local_unnamed_addr #0 {
  %3 = tail call i64 @strlen(i8* %0)
  %4 = tail call i64 @strlen(i8* %1)
  %5 = add i64 %3, 1
  %6 = add i64 %5, %4
  %7 = tail call i8* @malloc(i64 %6)
  %8 = icmp eq i8* %7, null
  br i1 %8, label %9, label %10

; <label>:9:                                      ; preds = %2
  tail call void @error()
  unreachable

; <label>:10:                                     ; preds = %2
  %11 = tail call i8* @strcpy(i8* nonnull %7, i8* %0)
  %12 = tail call i8* @strcat(i8* nonnull %7, i8* %1)
  ret i8* %7
}

define void @printString(i8* nocapture readonly) local_unnamed_addr #0 {
  %2 = tail call i32 @puts(i8* %0)
  ret void
}


!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"ecc version 2017-08-23 (http://ellcc.org) based on clang version 6.0.0 (trunk 311547)"}
!2 = !{!3, !3, i64 0}
!3 = !{!"any pointer", !4, i64 0}
!4 = !{!"omnipotent char", !5, i64 0}
!5 = !{!"Simple C/C++ TBAA"}
!6 = !{!7, !7, i64 0}
!7 = !{!"long", !4, i64 0}
!8 = !{!4, !4, i64 0}
!9 = !{!10, !10, i64 0}
!10 = !{!"int", !4, i64 0}