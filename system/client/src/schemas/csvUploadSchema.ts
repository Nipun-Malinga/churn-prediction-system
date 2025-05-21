import { z } from 'zod';

const csvUploadSchema = z.object({
  file: z.custom<FileList>((val) => val instanceof FileList && val.length > 0, {
    message: 'File is required',
  }),
});

export default csvUploadSchema;
